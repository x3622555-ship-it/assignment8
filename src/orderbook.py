# src/orderbook.py
"""
OrderBook
---------
Connects to Gateway (price + news server) at 127.0.0.1:9000
Receives framed messages (delimiter '*') and updates shared memory.
"""

import socket
import time
from src.shared_memory_utils import SharedPriceBook  # ✅ correct import for Option 1

HOST = "127.0.0.1"
PORT = 9000
DELIM = b"*"

# Symbols we expect from the Gateway
SYMBOLS = ["AAPL", "MSFT", "GOOG"]


class OrderBook:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None
        self.buffer = b""

        # Create shared memory to store latest prices
        self.spb = SharedPriceBook(SYMBOLS)
        print("✅ Shared memory created:", self.spb.names())

    # -----------------------------------------------------
    def connect(self):
        """Connect to the Gateway server, retry until successful."""
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                print(f"🔗 Connected to Gateway at {self.host}:{self.port}")
                break
            except ConnectionRefusedError:
                print("❌ Gateway not ready, retrying in 2 seconds...")
                time.sleep(2)

    # -----------------------------------------------------
    def run(self):
        """Main loop: receive framed messages and update shared memory."""
        try:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    print("⚠️  Disconnected from gateway.")
                    break

                self.buffer += data
                # Extract messages split by the delimiter '*'
                while DELIM in self.buffer:
                    msg, self.buffer = self.buffer.split(DELIM, 1)
                    self._handle_message(msg.decode().strip())

        except KeyboardInterrupt:
            print("\n🛑 Stopping OrderBook...")
        except Exception as e:
            print(f"Error in OrderBook: {e}")
        finally:
            self.cleanup()

    # -----------------------------------------------------
    def _handle_message(self, msg):
        """Parse and act on a single message frame."""
        parts = msg.split(",")
        if not parts:
            return

        if parts[0] == "PRICE" and len(parts) == 3:
            symbol, price_str = parts[1], parts[2]
            try:
                price = float(price_str)
                self.spb.update(symbol, price)
                print(f"📈 Updated {symbol} → {price:.2f}")
            except ValueError:
                print(f"⚠️  Invalid price format: {msg}")

        elif parts[0] == "NEWS":
            sentiment = parts[1] if len(parts) > 1 else "?"
            print(f"📰 News sentiment: {sentiment}")

        else:
            print(f"❓ Unknown message type: {msg}")

    # -----------------------------------------------------
    def cleanup(self):
        """Close sockets and release shared memory."""
        try:
            if self.sock:
                self.sock.close()
            self.spb.close()
            self.spb.unlink()
        except Exception:
            pass
        print("✅ Resources closed cleanly.")


# ---------------------------------------------------------
if __name__ == "__main__":
    ob = OrderBook()
    ob.connect()
    ob.run()
