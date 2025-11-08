# src/gateway.py
"""
Simple Gateway server that broadcasts price ticks and news sentiment.
- Runs on 127.0.0.1:9000 by default
- Message delimiter: b'*'
- Price format: PRICE,<SYMBOL>,<PRICE>*
- News format: NEWS,<SENTIMENT>*
"""

import socket
import threading
import time
import random
import json

HOST = "127.0.0.1"
PORT = 9000
MESSAGE_DELIMITER = b"*"

SYMBOLS = ["AAPL", "MSFT", "GOOG"]
TICK_INTERVAL = 0.2        # seconds between price ticks
NEWS_INTERVAL = 3.0        # seconds between news messages

class GatewayServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self._stop = threading.Event()
        # initialize synthetic prices
        self.prices = {s: 100.0 + random.random() * 10 for s in SYMBOLS}
        self._clients_lock = threading.Lock()

    def start(self):
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(8)
        print(f"Gateway listening on {self.host}:{self.port}")
        threading.Thread(target=self._accept_loop, daemon=True).start()
        threading.Thread(target=self._broadcast_loop, daemon=True).start()

    def _accept_loop(self):
        while not self._stop.is_set():
            try:
                client_sock, addr = self.server_sock.accept()
                print(f"Client connected: {addr}")
                with self._clients_lock:
                    self.clients.append(client_sock)
                # you can optionally spawn a thread to read from client if you expect messages
            except Exception as e:
                if not self._stop.is_set():
                    print("Accept error:", e)

    def _broadcast_loop(self):
        last_news = time.time()
        while not self._stop.is_set():
            now = time.time()
            # update prices with small random walk
            for s in SYMBOLS:
                self.prices[s] += (random.random() - 0.5) * 0.5  # small drift
            # send price messages (one per symbol)
            for s in SYMBOLS:
                msg = f"PRICE,{s},{self.prices[s]:.4f}".encode("utf-8") + MESSAGE_DELIMITER
                self._broadcast(msg)
            # occasionally send NEWS
            if now - last_news >= NEWS_INTERVAL:
                sentiment = random.randint(0, 100)
                msg = f"NEWS,{sentiment}".encode("utf-8") + MESSAGE_DELIMITER
                self._broadcast(msg)
                last_news = now
            time.sleep(TICK_INTERVAL)

    def _broadcast(self, data_bytes):
        with self._clients_lock:
            dead = []
            for c in self.clients:
                try:
                    c.sendall(data_bytes)
                except Exception:
                    dead.append(c)
            # remove dead clients
            for c in dead:
                try:
                    addr = c.getpeername()
                except Exception:
                    addr = "<unknown>"
                print(f"Client disconnected: {addr}")
                try:
                    self.clients.remove(c)
                    c.close()
                except Exception:
                    pass

    def stop(self):
        self._stop.set()
        try:
            self.server_sock.close()
        except Exception:
            pass
        with self._clients_lock:
            for c in self.clients:
                try:
                    c.close()
                except Exception:
                    pass
            self.clients.clear()


if __name__ == "__main__":
    g = GatewayServer()
    try:
        g.start()
        print("Gateway running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down gateway...")
        g.stop()
