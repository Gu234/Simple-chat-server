import threading
import socket
from utils import receive_json, send_json

def handle_client(connection):
    try:
        while True:
            recived_msg = receive_json(connection)
            print(recived_msg)
            send_json(connection, return_msg)
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
buffsize = 32
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
    s.close()
    print("Gracefully exiting.")

