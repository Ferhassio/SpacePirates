import socket
from session import Session
HOST = "localhost"
PORT = 5557


class Sever:
    def __init__(self, host, port):
        self.session = Session()
        self.host = host
        self.port = port
        self.flag = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as error:
            self.socket.close()
            print(str(error))

    def start(self):
        self.socket.listen(4)
        print(f'Server started at {self.host}:{self.port}')
        while self.flag:
            client, address = self.socket.accept()
            print('Connected:', address)
            print('Connection info:', client)
            response = self.send('Handshake from server', client)
            self.send(self.session.add(response.decode('utf-8')), client)
            print('Current session:', self.session)

    @staticmethod
    def send(data, client):
        try:
            client.send(str.encode(data))
            return client.recv(2048 * 2)
        except socket.error as e:
            print(e)

    def __del__(self):
        self.socket.close()


if __name__ == '__main__':
    test_serv = Sever(HOST, PORT)
    test_serv.start()
