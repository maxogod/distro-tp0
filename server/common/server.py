import socket
import logging

import common.bet_protocol as bet_protocol
import common.utils as utils


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        while True:
            client_sock = self.__accept_new_connection()
            protocol = bet_protocol.BetProtocol(client_sock)
            try:
                bet = protocol.receive_bet()
                utils.store_bets([bet])
                logging.info(
                    f"action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}"
                )
                protocol.send_bet_confirmation()
            except (OSError, EOFError, RuntimeError) as e:
                logging.error(f"action: receive_message | result: fail | error: {e}")
            finally:
                protocol.shutdown()

    def shutdown(self):
        self._server_socket.close()

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
