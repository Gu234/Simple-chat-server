import socket
import time
import itertools as it
from utils import receive_json, send_json, dispatch_handler

def handle_client(connection, msgs):
    try:
        while True:
            recived_msg = receive_json(connection)
            print(recived_msg)
            msgs.append(recived_msg)
    except ConnectionError:
        print("The connection was dropped")

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


host = 'localhost'
port = 4800
addr = (host,port)
buffsize = 32
msgs_to_send = []
connections = {}
counter = it.count()
s = socket.socket()
s.settimeout(5)
s.bind(addr)
print('binded socket to address:' , addr)
s.listen(2)
print('socket is listening')
try:
    dispatch_handler(connections, msgs_to_send, handle_msg_sending)
    while True:
        try:
            connection, client_addr = s.accept()
            connections[next(counter)] = connection
            dispatch_handler(connection, msgs_to_send, handle_client)
        except socket.timeout:
            pass
except KeyboardInterrupt:
    s.close()
    print("Gracefully exiting.")

