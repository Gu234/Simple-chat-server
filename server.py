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
        self.user_names = {}
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
                    current_user_id = next(counter)
                    self.connections[current_user_id] = connection
                    self.user_names[current_user_id] = self.receive_user_name(connection)
                    self.broadcast_new_user(current_user_id)

                    dispatch_handler(ChatServer.handle_client, (self, connection, current_user_id))
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            self.server_socket.close()
            print("Gracefully exiting.")

    @staticmethod
    def handle_client(chat_server, connection, user_id):
        try:
            while True:
                received_msg = receive_json(connection)
                print(received_msg)
                chat_server.msgs_to_send.append(received_msg)
        except ConnectionError:
            chat_server.broadcast_user_leaving(user_id)
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

    def receive_user_name(self, connection):
        try:
            recived_msg = receive_json(connection)
            return recived_msg['user_name']
        except ConnectionError:
            print('Connection Error while getting user name.')
        except KeyError:
            return 'anonymous'

    def broadcast_new_user(self, user_id):
        user_name = self.user_names[user_id]
        msg = {
            'user_name': 'SERVER',
            'text': f'{user_name} has joined the chat.'
        }
        self.msgs_to_send.append(msg)

    def broadcast_user_leaving(self, user_id):
        user_name = self.user_names[user_id]
        msg = {
            'user_name': 'SERVER',
            'text': f'{user_name} has left the chat.'
        }
        self.msgs_to_send.append(msg)


if __name__ == '__main__':
    server = ChatServer()
    server.run()
