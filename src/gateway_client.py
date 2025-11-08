# src/gateway_client.py
import socket

HOST = "127.0.0.1"
PORT = 9000
DELIM = b'*'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print("Connected to gateway. Receiving 10 messages...")

buffer = b""
count = 0
try:
    while count < 10:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buffer += chunk
        while DELIM in buffer:
            msg, buffer = buffer.split(DELIM, 1)
            print("MSG:", msg.decode())
            count += 1
finally:
    sock.close()
    print("Client done.")
