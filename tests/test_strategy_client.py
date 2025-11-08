# src/test_strategy_client.py
import socket, json, time

HOST, PORT = "127.0.0.1", 9001
DELIM = b"*"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print("Connected to OrderManager.")

orders = [
    {"symbol": "AAPL", "side": "BUY", "qty": 5, "price": 171.25},
    {"symbol": "MSFT", "side": "SELL", "qty": 10, "price": 328.10},
]

for order in orders:
    msg = json.dumps(order).encode("utf-8") + DELIM
    sock.sendall(msg)
    print("Sent order:", order)
    time.sleep(0.5)
    data = sock.recv(1024)
    print("Reply:", data.decode())

sock.close()
print("Client done.")
