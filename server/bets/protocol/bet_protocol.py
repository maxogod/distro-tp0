import socket
import bets.utils as utils
from bets.models.bet import Bet
from bets.protocol.consts import *
from bets.protocol.errors import *

class BetProtocol:
    def __init__(self, skt: socket.socket) -> None:
        self._skt = skt

    def shutdown(self) -> None:
        """ Closes the connection with the client. """
        if self._skt.fileno() != -1:
            self._skt.shutdown(socket.SHUT_RDWR)
            self._skt.close()

    def receive_bet_batch(self) -> list[Bet]:
        """ Receives a batch of bets from client and returns them. """

        # [HEADER][BATCH_SIZE][BET1_LEN][BET1]...[BETN_LEN][BETN]
        header = int.from_bytes(self.__read_full(PROTOCOL_HEADER_SIZE), byteorder='big')
        if header != BET_DATA_HEADER:
            raise ValueError("Received invalid header.")

        batch_size_bytes = self.__read_full(BET_LENGTH_SIZE)
        batch_size = int.from_bytes(batch_size_bytes, byteorder='big')

        bets = []
        for _ in range(batch_size):
            msg_len_bytes = self.__read_full(BET_LENGTH_SIZE)
            msg_len = int.from_bytes(msg_len_bytes, byteorder='big')

            msg_bytes = self.__read_full(msg_len)
            msg_str = msg_bytes.decode('utf-8')

            try:
                first_name, last_name, document, birthdate, number = msg_str.split('|')
                bets.append(Bet("1", first_name, last_name, document, birthdate, number))
            except ValueError:
                continue # Ignore malformed bets

        if len(bets) != batch_size:
            raise InconsistentBatchSizeError(batch_size)

        return bets

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
                raise ConnectionClosedError("Socket connection closed.")
            bytes_received += chunk_size
        return bytes(buff)


    def __write_full(self, data: bytes) -> None:
        view = memoryview(data)
        bytes_sent = 0
        n = len(data)
        while bytes_sent < n:
            chunk_size = 0
            try:
                chunk_size = self._skt.send(view[bytes_sent:])
            except (BrokenPipeError, ConnectionResetError):
                raise ConnectionClosedError("Socket connection closed.")
            bytes_sent += chunk_size
