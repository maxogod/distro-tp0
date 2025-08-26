import socket
import logging
import bets.protocol.bet_protocol as bet_protocol
import bets.utils as utils


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        self._client_conn = None

    def run(self):
        """ Main server logic loop. """
        self._running = True

        while self._running:
            try:
                client_socket = self.__accept_new_connection()
            except OSError as e:
                logging.error(f"action: accept_connections | result: fail | error: {e}")
                continue

            self._client_conn = bet_protocol.BetProtocol(client_socket)
            try:
                bet = self._client_conn.receive_bet()
                utils.store_bets([bet])
                logging.info(
                    f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}"
                )
                self._client_conn.send_bet_confirmation()
            except (OSError, EOFError, RuntimeError) as e:
                logging.error(f"action: client_bet_communication | result: fail | error: {e}")
            finally:
                self._client_conn.shutdown()
                self._client_conn = None

    def shutdown(self):
        """ Stop running server and close any communication. """
        self._running = False
        self._server_socket.close()

        if self._client_conn is not None:
            self._client_conn.shutdown()

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
