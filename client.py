import socket
import json

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
            break
        if user_input == '':
            continue
        s.send(json.dumps(msg).encode())
        server_response = s.recv(buffsize)
        print(server_response.decode())
except ConnectionError:
    print('Connection dropped')



