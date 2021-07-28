import json
import threading

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

def dispatch_handler(connection, msgs, target):
    new_thread = threading.Thread(target=target, args=(connection, msgs))
    new_thread.setDaemon(True)
    new_thread.start()
    return new_thread

