import socket
import time


class Client:
    def __init__(self, server: str, host: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (server, int(host))

    def set_name(self, player_name):
        self.client.send(str.encode(player_name))

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except Exception as err:
            print(str(err))

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048 * 2)
        except socket.error as e:
            print(e)

    def close(self):
        self.client.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    new_cl = Client('localhost', 5557)
    print(new_cl.connect())
    time.sleep(2)
    name = input('Set a name:')
    result = new_cl.send(name)
    print(result)



