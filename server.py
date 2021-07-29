import socket
import time
import itertools as it
from utils import receive_json, send_json, dispatch_handler


class ChatServer():

    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 4800
        self.addr = (self.host, self.port)
        self.msgs_to_send = []
        self.connections = {}
        self.initialize_socket()

    def initialize_socket(self):
        self.server_socket = socket.socket()
        self.server_socket.settimeout(5)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(2)

    def run(self):
        counter = it.count()
        print('server is up and running')
        try:
            dispatch_handler(ChatServer.handle_msg_sending, (self.connections, self.msgs_to_send))
            while True:
                try:
                    connection, client_addr = self.server_socket.accept()
                    self.connections[next(counter)] = connection
                    dispatch_handler(ChatServer.handle_client, (connection, self.msgs_to_send))
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            self.server_socket.close()
            print("Gracefully exiting.")

    @staticmethod
    def handle_client(connection, msgs):
        try:
            while True:
                recived_msg = receive_json(connection)
                print(recived_msg)
                msgs.append(recived_msg)
        except ConnectionError:
            print("The connection was dropped")

    @staticmethod
    def handle_msg_sending(connections, msgs):
        while True:
            if msgs != []:
                inactive_connections = []
                for key, connection in connections.items() :
                    try:
                        send_json(connection, msgs[0])
                    except ConnectionError:
                        inactive_connections.append(key)
                        print("msg wasn't sent due to connection error")
                msgs.pop(0)
                for key in inactive_connections:
                    connections.pop(key)
            time.sleep(1)

if __name__ == '__main__':
    server = ChatServer()
    server.run()
