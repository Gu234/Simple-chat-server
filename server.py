from os import error
import threading
import socket

def handle_client(connection):
    try:
        while True:
            byte_msg = connection.recv(buffsize)
            print(byte_msg.decode())
            connection.send(return_msg.encode())
    except ConnectionError:
        print("The connection was dropped")
            

def dispatch_handler(connection):
    new_thread = threading.Thread(target=handle_client, args=(connection,))
    new_thread.setDaemon(True)
    new_thread.start()
    return new_thread
    
host = 'localhost'
port = 4800
addr = (host,port)
buffsize = 4096
return_msg = 'Roger dogger!'

s = socket.socket()
s.settimeout(5)
s.bind(addr)
print('binded socket to address:' , addr)
s.listen(2)
print('socket is listening')
try:
    while True:
        try:
            connection, client_addr = s.accept()
            dispatch_handler(connection)
        except socket.timeout:
            pass
except KeyboardInterrupt:
    print("Gracefully exiting.")

