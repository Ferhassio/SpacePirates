import socket
from session import Session
HOST = "0.0.0.0"
PORT = 4004


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
            response = self.send(f'[SERVER] Client {address} connected.', client)
            print(address, response.decode('utf-8'))
            self.session.add(response.decode('utf-8'), client)

            # self.send(self.session.add(response.decode('utf-8')), client)
            # print('Current session:', self.session)

    @staticmethod
    def send(data, client):
        try:
            client.send(str.encode(data))
            return client.recv(2048 * 2)
        except socket.error as e:
            print(e)

    def clientthread(self, conn, addr):
        # sends a message to the client whose user object is conn
        conn.send("Welcome to this chatroom!")

        while True:
            try:
                message = conn.recv(2048)
                if message:

                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print("<" + addr[0] + "> " + message)

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + addr[0] + "> " + message
                    # broadcast(message_to_send, conn)
                    self.se

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    # Remove from session
                    self.session.remove(message)

            except:
                continue


    def __del__(self):
        self.socket.close()


if __name__ == '__main__':
    test_serv = Sever(HOST, PORT)
    test_serv.start()
