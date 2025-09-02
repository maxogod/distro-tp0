import socket
import sys
import logging
from bets.protocol.bet_protocol import BetProtocol
import bets.utils as utils
from bets.protocol.errors import InconsistentBatchSizeError, ConnectionClosedError


class Server:
    def __init__(self, port, listen_backlog, agencies_amount):
        self._agencies_amount = agencies_amount

        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        self._clients_connected: dict[int, BetProtocol | None] = {}

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

            agency_id = client_conn.receive_agency_id()
            self._clients_connected[agency_id] = client_conn
            while self._clients_connected.get(agency_id) is not None:
                try:
                    batch = client_conn.receive_bet_batch()
                    if not batch:
                        break # No more bets from agency

                    logging.info(f"action: apuesta_recibida | result: success | cantidad: {len(batch)}")

                    utils.store_bets(batch)
                    client_conn.send_bet_confirmation()
                except InconsistentBatchSizeError as e:
                    logging.error(f"action: apuesta_recibida | result: fail | cantidad: {e.size_expected}")
                except ConnectionClosedError as e:
                    client_conn.shutdown()
                    self._clients_connected[agency_id] = None
                # Make sure logs are written
                sys.stdout.flush()
                sys.stderr.flush()

        logging.info("action: sorteo | result: success")
        winner_ids_per_agency: dict[int, list[int]] = {}
        for bet in utils.load_bets():
            if utils.has_won(bet):
                if bet.agency not in winner_ids_per_agency:
                    winner_ids_per_agency[bet.agency] = []
                winner_ids_per_agency[bet.agency].append(int(bet.document))

        for agency_id, conn in self._clients_connected.items():
            if not conn: continue
            conn.send_winner_ids(winner_ids_per_agency.get(agency_id, []))

    def shutdown(self):
        """ Stop running server and close any communication. """
        self._running = False
        self._server_socket.close()

        for agency_id, conn in self._clients_connected.items():
            if not conn: continue
            conn.shutdown()
            self._clients_connected[agency_id] = None
            
    def __are_agencies_remaining(self):
        return len(self._clients_connected) < self._agencies_amount

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
