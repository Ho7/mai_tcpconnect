import random
import socket


class Game:
    _default_port = 8000
    _default_scope = (1, 10)
    _default_host = '127.0.0.1'
    _default_listen_count = 1
    _DATA_COUNT = 1024
    _SUCCESS_COMMAND = 'guess'

    def __init__(self, host: str = None, port: int = None, scope: list = None, listen_count: int = None):
        self.host = host or self._default_host
        self.port = port or self._default_port
        self.scope = scope or self._default_scope
        self.listen_count = listen_count or self._default_listen_count

    def _get_hidden_number(self):
        return random.randint(self.scope[0], self.scope[1])

    def run_connect(self):
        sock = socket.socket()
        sock.bind((self.host, self.port))
        sock.listen(self.listen_count)
        connect, _ = sock.accept()
        hidden_number = self._get_hidden_number()

        while True:
            raw_data = connect.recv(self._DATA_COUNT)

            if not raw_data:
                connect.close()
                break

            command, argument = self._decode_data(raw_data)

            if command == self._SUCCESS_COMMAND:
                result = self._check_user_number(hidden_number, argument)
                connect.send(self._encode_data(result))
            else:
                connect.send(self._encode_data('Неверная команда'))
                connect.close()
                break

    @staticmethod
    def _check_user_number(hidden_number: int, user_number: int):
        if user_number == hidden_number:
            return 'correct'
        elif user_number > hidden_number:
            return 'more'
        elif user_number < hidden_number:
            return 'less'

    @staticmethod
    def _decode_data(data: bytes):
        prepare_data = data.decode('utf-8').split(',')
        return prepare_data[0], int(prepare_data[1])

    @staticmethod
    def _encode_data(data: str):
        return data.encode('utf-8')

    
if __name__ == "__main__":
    Game().run_connect()
