# src/ordermanager.py
"""
OrderManager
-------------
Listens for order messages from Strategy clients.
Each message is JSON-encoded and delimited by '*'.

Example message from Strategy:
{"symbol": "AAPL", "side": "BUY", "qty": 10, "price": 172.50}*
"""

import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 9001
DELIM = b"*"


class OrderManager:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self._stop = threading.Event()
        print(f"✅ OrderManager initialized on {self.host}:{self.port}")

    # ----------------------------------------------------------
    def start(self):
        """Start the OrderManager server."""
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(8)
        print(f"📦 OrderManager listening on {self.host}:{self.port}")

        while not self._stop.is_set():
            try:
                client_sock, addr = self.server_sock.accept()
                print(f"🔗 Strategy connected from {addr}")
                threading.Thread(
                    target=self._handle_client, args=(client_sock, addr), daemon=True
                ).start()
            except Exception as e:
                if not self._stop.is_set():
                    print("❌ Accept error:", e)

    # ----------------------------------------------------------
    def _handle_client(self, sock, addr):
        """Handle incoming messages from one Strategy client."""
        buffer = b""
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    print(f"⚠️ Strategy disconnected: {addr}")
                    break
                buffer += data

                while DELIM in buffer:
                    msg, buffer = buffer.split(DELIM, 1)
                    self._process_order(msg, sock)
        except Exception as e:
            print(f"❌ Connection error with {addr}: {e}")
        finally:
            sock.close()

    # ----------------------------------------------------------
    def _process_order(self, msg_bytes, sock):
        """Decode and log a JSON order message."""
        try:
            msg_str = msg_bytes.decode("utf-8").strip()
            order = json.loads(msg_str)
            print(f"📝 Received order: {order}")

            # Simple validation example
            if all(k in order for k in ("symbol", "side", "qty", "price")):
                confirmation = {
                    "status": "ACCEPTED",
                    "symbol": order["symbol"],
                    "side": order["side"],
                    "qty": order["qty"],
                    "price": order["price"],
                }
            else:
                confirmation = {"status": "REJECTED", "reason": "Missing fields"}

            # Send back confirmation
            response = json.dumps(confirmation).encode("utf-8") + DELIM
            sock.sendall(response)
            print(f"📤 Sent confirmation: {confirmation}")

        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON message: {msg_bytes}")
        except Exception as e:
            print(f"❌ Error processing order: {e}")

    # ----------------------------------------------------------
    def stop(self):
        """Stop the OrderManager server."""
        self._stop.set()
        try:
            self.server_sock.close()
        except Exception:
            pass
        print("✅ OrderManager stopped.")


if __name__ == "__main__":
    om = OrderManager()
    try:
        om.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down OrderManager...")
        om.stop()
