from json.decoder import JSONDecodeError
import threading
import socket
import json

def handle_client(connection):
    try:
        all_chunks = b''
        while True:
            byte_msg = connection.recv(buffsize)
            all_chunks += byte_msg
            try:
                recived_msg = json.loads(all_chunks.decode())
                all_chunks = b''
                print(recived_msg)
                connection.send(return_msg.encode())
            except JSONDecodeError:
                continue

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
return_msg = json.dumps('Roger dogger!')

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

