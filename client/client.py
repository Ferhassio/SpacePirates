import socket
import time


class Client:
    def __init__(self, server: str, host: int, login: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (server, int(host))
        self.connect()
        self.set_name(login)
        # self.receive()

    def set_name(self, player_name):
        return self.client.send(str.encode(player_name))

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except Exception as err:
            print(str(err))

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048 * 8)
        except socket.error as e:
            print(e)

    # def receive(self):
    #     flag = True
    #     retry = 0
    #     while flag:
    #         if retry != 10:
    #             try:
    #                 flag = False
    #                 message = self.client.recv(2048 * 8)
    #                 if message:
    #                     return message
    #                 else:
    #                     retry += 1
    #                     time.sleep(.5)
    #             except socket.error as e:
    #                 print(e)
    #         else:
    #             break


    def close(self):
        self.client.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    new_cl = Client('localhost', 5557, 'tetset')
    print(new_cl.connect())
    time.sleep(2)
    name = input('Set a name:')
    result = new_cl.send(name)
    print(result)



