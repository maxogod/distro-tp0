import socket
import sys
import logging
import multiprocessing
from bets.protocol.bet_protocol import BetProtocol
import bets.utils as utils
from bets.protocol.errors import InconsistentBatchSizeError, ConnectionClosedError


class Server:
    def __init__(self, port, listen_backlog, agencies_amount):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        self._agencies_amount = agencies_amount
        
        # Multiprocessing
        self._bet_storage_lock = multiprocessing.Lock()
        self._lottery_start_barrier = multiprocessing.Barrier(agencies_amount)
        self._shutdown_event = multiprocessing.Event()
        self._processes = []

    def __del__(self):
        self.shutdown()

    def run(self):
        """ Main server logic loop. """
        self._running = True

        while self._running and self.__are_agencies_remaining():
            try:
                client_socket = self.__accept_new_connection()
            except OSError as e:
                logging.error(f"action: accept_connections | result: fail | error: {e}")
                break

            client_conn: BetProtocol = BetProtocol(client_socket)

            # Receive current agency ID
            try:
                agency_id = client_conn.receive_agency_id()
            except ConnectionClosedError as e:
                continue # Next client

            # Handle new agency communication in a new process
            p = multiprocessing.Process(target=self.__handle_agency_connection, args=(agency_id, client_conn))
            p.start()
            self._processes.append(p)

        for p in self._processes:
            p.join()

    def shutdown(self):
        """ Stop running server and close any communication. """
        self._running = False
        self._server_socket.close()

        self._shutdown_event.set()
        for p in self._processes:
            p.join()

    def __handle_agency_connection(self, agency_id, conn: BetProtocol):
        """ Connection handler for each agency, to be run in a separate process. """

        while not conn.is_closed() and not self._shutdown_event.is_set():
            try:
                batch = conn.receive_bet_batch()
                if not batch:
                    break # No more bets from agency

                logging.info(f"action: apuesta_recibida | result: success | cantidad: {len(batch)}")

                with self._bet_storage_lock:
                    utils.store_bets(batch)

                conn.send_bet_confirmation()
            except InconsistentBatchSizeError as e:
                logging.error(f"action: apuesta_recibida | result: fail | cantidad: {e.size_expected}")
            except ConnectionClosedError as e:
                conn.shutdown()

            # Make sure logs are written
            sys.stdout.flush()
            sys.stderr.flush()

        # Wait for all agencies to finish sending bets
        self._lottery_start_barrier.wait()

        if conn.is_closed():
            return
        elif self._shutdown_event.is_set():
            conn.shutdown()
            return

        logging.info("action: sorteo | result: success")
        winner_ids: list[int] = []
        for bet in utils.load_bets(): # Safe multi-process read opearation
            if bet.agency == agency_id and utils.has_won(bet):
                winner_ids.append(int(bet.document))

        try:
            conn.send_winner_ids(winner_ids)
        except ConnectionClosedError as e:
            pass

        conn.shutdown()

    def __are_agencies_remaining(self):
        return len(self._processes) < self._agencies_amount
            
    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(
            f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
