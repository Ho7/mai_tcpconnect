import socket


class Gamer:
    _default_host = '127.0.0.1'
    _default_port = 8000
    _DEFAULT_COMMAND = 'guess'
    _DATA_COUNT = 1024
    _SUCCESS_RESPONSE = 'correct'

    def __init__(self, host: str = None, port: int = None):
        self.host = host or self._default_host
        self.port = port or self._default_port

    def run_connect(self):
        sock = socket.socket()
        sock.connect((self.host, self.port))

        while True:
            user_number = input('Введите число: ')
            send_str = f'{self._DEFAULT_COMMAND}, {user_number}'
            sock.send(self.encode_data(send_str))

            raw_data = sock.recv(self._DATA_COUNT)
            data = self.decode_data(raw_data)
            print(data)

            if data == self._SUCCESS_RESPONSE:
                sock.close()
                break

    @staticmethod
    def encode_data(data: str):
        return data.encode('utf-8')

    @staticmethod
    def decode_data(data: bytes):
        return data.decode('utf-8')


if __name__ == "__main__":
    Gamer().run_connect()
