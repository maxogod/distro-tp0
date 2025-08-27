import socket
import bets.utils as utils
from bets.protocol.consts import *

class BetProtocol:
    def __init__(self, skt: socket.socket) -> None:
        self._skt = skt

    def shutdown(self) -> None:
        """ Closes the connection with the client. """
        if self._skt.fileno() != -1:
            self._skt.shutdown(socket.SHUT_RDWR)
            self._skt.close()

    def receive_bet(self) -> utils.Bet:
        """ Receives a bet from client and returns it. """
        header = int.from_bytes(self.__read_full(PROTOCOL_HEADER_SIZE), byteorder='big')
        if header != BET_DATA_HEADER:
            raise ValueError("Received invalid header.")

        msg_len_bytes = self.__read_full(BET_LENGTH_SIZE)
        msg_len = int.from_bytes(msg_len_bytes, byteorder='big')

        msg_bytes = self.__read_full(msg_len)
        msg_str = msg_bytes.decode('utf-8')

        first_name, last_name, document, birthdate, number = msg_str.split('|')
        return utils.Bet("1", first_name, last_name, document, birthdate, number)

    def send_bet_confirmation(self) -> None:
        """ Sends a bet confirmation to the client. """
        confirmation_code_bytes = BET_CONFIRMATION_HEADER.to_bytes(length=1, byteorder='big')
        self.__write_full(confirmation_code_bytes)
    
    def __read_full(self, n: int) -> bytes:
        buff = bytearray(n)
        view = memoryview(buff)
        bytes_received = 0
        while bytes_received < n:
            chunk_size = self._skt.recv_into(view[bytes_received:])
            if chunk_size == 0:
                raise EOFError("Socket connection closed.")
            bytes_received += chunk_size
        return bytes(buff)


    def __write_full(self, data: bytes) -> None:
        view = memoryview(data)
        bytes_sent = 0
        n = len(data)
        while bytes_sent < n:
            chunk_size = self._skt.send(view[bytes_sent:])
            if chunk_size == 0:
                raise RuntimeError("Socket connection broken.")
            bytes_sent += chunk_size
