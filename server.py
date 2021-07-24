from os import error
import socket

host = 'localhost'
port = 4800
addr = (host,port)
buffsize = 4096
return_msg = 'Roger dogger!'

print('')
s = socket.socket()
s.settimeout(5)
print('')
s.bind(addr)
print('binded socket to address:' , addr)
s.listen(1)
print('socket is listening')
try:
    while True:
        try:
            connection, client_addr = s.accept()
            while True:
                byte_msg = connection.recv(buffsize)
                print(byte_msg.decode())
                connection.send(return_msg.encode())
        except ConnectionError as e:
            print("The connection was dropped")
        except socket.timeout:
            pass

except KeyboardInterrupt:
    print("Gracefully exiting.")
