import socket

from server.common import utils

BET_CONFIRMATION_CODE = 0x01

class BetProtocol:
    def __init__(self, skt: socket.socket) -> None:
        self._skt = skt

    def shutdown(self) -> None:
        self._skt.close()

    def receive_bet(self) -> utils.Bet:
        msg_len_bytes = self.__read_full(4)
        msg_len = int.from_bytes(msg_len_bytes, byteorder='big')
        msg_bytes = self.__read_full(msg_len)
        msg_str = msg_bytes.decode('utf-8')
        first_name, last_name, document, birthdate, number = msg_str.split('|')
        return utils.Bet("1", first_name, last_name, document, birthdate, number)

    def send_bet_confirmation(self) -> None:
        confirmation_code_bytes = BET_CONFIRMATION_CODE.to_bytes(1, byteorder='big')
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
