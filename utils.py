import json
import socket


def receive_json(connection, buffsize=32):
    chunks = b''
    while True:
        chunk = connection.recv(buffsize)
        if chunk == b'':
            raise ConnectionError
        chunks += chunk
        try:
            return json.loads(chunks.decode())
        except json.JSONDecodeError:
            continue

def send_json(connection, payload):
    connection.send(json.dumps(payload).encode())



