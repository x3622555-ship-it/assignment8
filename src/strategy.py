# src/strategy.py
"""
Strategy
---------
Connects to:
- Gateway (price + news feed) at 127.0.0.1:9000
- OrderManager (order receiver) at 127.0.0.1:9001

Implements a simple trading logic:
- BUY if price < 100
- SELL if price > 105
"""

import socket
import json
import time

# Connection constants
HOST_GATEWAY = "127.0.0.1"
PORT_GATEWAY = 9000
HOST_ORDERMANAGER = "127.0.0.1"
PORT_ORDERMANAGER = 9001
DELIM = b"*"


class Strategy:
    def __init__(self):
        self.gw_sock = None
        self.om_sock = None
        self.buffer = b""
        self.positions = {}  # symbol -> position size
        print("✅ Strategy initialized")

    # --------------------------------------------------------
    def connect_gateway(self):
        """Connect to the Gateway for live data."""
        while True:
            try:
                self.gw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.gw_sock.connect((HOST_GATEWAY, PORT_GATEWAY))
                print(f"🔗 Connected to Gateway at {HOST_GATEWAY}:{PORT_GATEWAY}")
                break
            except ConnectionRefusedError:
                print("❌ Gateway not ready, retrying in 2s...")
                time.sleep(2)

    # --------------------------------------------------------
    def connect_ordermanager(self):
        """Connect to the OrderManager to send orders."""
        while True:
            try:
                self.om_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.om_sock.connect((HOST_ORDERMANAGER, PORT_ORDERMANAGER))
                print(f"🔗 Connected to OrderManager at {HOST_ORDERMANAGER}:{PORT_ORDERMANAGER}")
                break
            except ConnectionRefusedError:
                print("❌ OrderManager not ready, retrying in 2s...")
                time.sleep(2)

    # --------------------------------------------------------
    def run(self):
        """Main loop: receive market data and trade."""
        try:
            while True:
                data = self.gw_sock.recv(1024)
                if not data:
                    print("⚠️ Disconnected from Gateway.")
                    break

                self.buffer += data
                while DELIM in self.buffer:
                    msg, self.buffer = self.buffer.split(DELIM, 1)
                    self._handle_message(msg.decode().strip())

        except KeyboardInterrupt:
            print("\n🛑 Strategy stopped by user.")
        except Exception as e:
            print(f"❌ Strategy error: {e}")
        finally:
            self.cleanup()

    # --------------------------------------------------------
    def _handle_message(self, msg):
        """Process each message from the Gateway."""
        parts = msg.split(",")
        if not parts:
            return

        if parts[0] == "PRICE" and len(parts) == 3:
            symbol = parts[1]
            try:
                price = float(parts[2])
                print(f"📊 {symbol} price: {price:.2f}")
                self._maybe_trade(symbol, price)
            except ValueError:
                print(f"⚠️ Invalid price message: {msg}")

        elif parts[0] == "NEWS":
            sentiment = parts[1] if len(parts) > 1 else "?"
            print(f"📰 News sentiment: {sentiment}")

        else:
            print(f"❓ Unknown message: {msg}")

    # --------------------------------------------------------
    def _maybe_trade(self, symbol, price):
        """Very simple trading logic."""
        position = self.positions.get(symbol, 0)

        if price < 100 and position <= 0:
            self._send_order(symbol, "BUY", 10, price)
            self.positions[symbol] = 10
        elif price > 105 and position > 0:
            self._send_order(symbol, "SELL", 10, price)
            self.positions[symbol] = 0

    # --------------------------------------------------------
    def _send_order(self, symbol, side, qty, price):
        """Send a trade order to the OrderManager."""
        order = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": round(price, 2)
        }

        msg = json.dumps(order).encode("utf-8") + DELIM

        try:
            self.om_sock.sendall(msg)
            print(f"📤 Sent order: {order}")

            # Wait for confirmation
            data = self.om_sock.recv(1024)
            if data:
                responses = data.decode().split("*")
                for res in responses:
                    if res.strip():
                        print(f"✅ Confirmation: {res}")
        except Exception as e:
            print(f"⚠️ Failed to send order: {e}")

    # --------------------------------------------------------
    def cleanup(self):
        """Close connections gracefully."""
        try:
            if self.gw_sock:
                self.gw_sock.close()
            if self.om_sock:
                self.om_sock.close()
        except Exception:
            pass
        print("✅ Strategy cleanup complete.")


# --------------------------------------------------------
# ✅ Main block to run the strategy
if __name__ == "__main__":
    strat = Strategy()
    strat.connect_gateway()
    strat.connect_ordermanager()
    strat.run()
