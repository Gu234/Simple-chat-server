import socket
from utils import receive_json, send_json, dispatch_handler


class ChatClient:
    host = 'localhost'
    port = 4800
    address = (host,port)

    def __init__(self) -> None:
        self.user_name = 'annonymous'
        self.msg = {}
        self.msg['user_name'] = self.user_name
        self.socket = None

    def run(self):
        self.ask_user_name()
        self.create_socket()
        try:
            self.socket.connect(ChatClient.address)
            print('connected')
            self.send_name()
        except ConnectionError:
            print('failed to connect to server.')
            return

        dispatch_handler(ChatClient.handle_incoming_msgs, (self.socket, ) )
        self.msg_loop()

    @staticmethod
    def handle_incoming_msgs(connection):
        try:
            while True:
                incoming_data = receive_json(connection)
                print(f"{incoming_data['user_name']}: {incoming_data['text']}")
        except ConnectionError:
            print("The connection was dropped")

    def send_name(self):
        send_json(self.socket, self.msg)

    def ask_user_name(self):
        self.user_name = input('Enter your name: ')
        self.msg['user_name'] = self.user_name

    def create_socket(self):
        if self.socket is None:
            self.socket = socket.socket()
    
    def get_msg(self):
        user_input = input('')
        self.msg['text'] = user_input

    def msg_loop(self):
        try:
            while True:
                self.get_msg()
                if self.msg['text'] == 'exit':
                    print("Exiting...")
                    self.socket.close()
                    break
                if self.msg['text'] == '':
                    continue
                send_json(self.socket, self.msg)

        except ConnectionError:
            print('Connection dropped')
            self.socket.close()


if __name__ == '__main__':
    client = ChatClient()
    client.run()