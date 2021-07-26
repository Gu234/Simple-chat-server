import socket
from utils import receive_json, send_json


host = 'localhost'
port = 4800
addr = (host,port)
msg = {}
buffsize = 4096

s = socket.socket()
print('created a socket')

s.connect(addr)
print('connected')

try:
    while True:
        user_input = input('Ur msg to teh serva:')
        msg['text'] = user_input

        if user_input == 'exit':
            s.close()
            break
        if user_input == '':
            continue
        
        send_json(s, msg)
        server_response = receive_json(s)
        print(server_response)

except ConnectionError:
    print('Connection dropped')



