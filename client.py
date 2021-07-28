import socket
from utils import receive_json, send_json, dispatch_handler

user_name = input('Enter your name: ')
host = 'localhost'
port = 4800
addr = (host,port)
msg = {}
msg['user_name'] = user_name

buffsize = 4096

s = socket.socket()
print('created a socket')

s.connect(addr)
print('connected')

def handle_incoming_msgs(connection, msgs):
    try:
        while True:
            incoming_data = receive_json(connection)
            print(f"{incoming_data['user_name']}: {incoming_data['text']}")
    except ConnectionError:
        print("The connection was dropped")

try:
    dispatch_handler(s, None, handle_incoming_msgs)
    while True:
        user_input = input('')
        msg['text'] = user_input
        if user_input == 'exit':
            s.close()
            break
        if user_input == '':
            continue
        
        send_json(s, msg)

except ConnectionError:
    print('Connection dropped')
    s.close()



