import socket

host = 'localhost'
port = 4800
addr = (host,port)
msg = 'Hello this is Mark.'
buffsize = 4096

byte_msg = msg.encode()
s = socket.socket()
print('created a socket')

s.connect(addr)
print('connected')

try:
    while True:
        user_input = input('Ur msg to teh serva:')
        if user_input == 'exit':
            break
        if user_input == '':
            continue
        s.send(user_input.encode())
        server_response = s.recv(buffsize)
        print(server_response.decode())
except ConnectionError:
    print('Connection dropped')



