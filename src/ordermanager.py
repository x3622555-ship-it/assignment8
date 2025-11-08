import time
import json
import logging
from datetime import datetime

# Configure trade log
trade_logger = logging.getLogger("trades")
trade_logger.setLevel(logging.INFO)
trade_handler = logging.FileHandler("trades.log", mode="a")
trade_formatter = logging.Formatter("%(asctime)s - %(message)s")
trade_handler.setFormatter(trade_formatter)
trade_logger.addHandler(trade_handler)

class OrderManager:
    def __init__(self, host="127.0.0.1", port=9001):
        self.host = host
        self.port = port
        self.sent_orders = []  # Track all orders

    def send_order(self, order):
        print(f"📤 Sent order: {order}")
        trade_logger.info(f"Sent order: {order}")

        confirmation = {
            "status": "ACCEPTED",
            "symbol": order["symbol"],
            "side": order["side"],
            "qty": order["qty"],
            "price": order["price"]
        }

        self.sent_orders.append(order)
        time.sleep(0.5)  # simulate delay

        confirmation_json = json.dumps(confirmation)
        print(f"✅ Confirmation: {confirmation_json}")
        trade_logger.info(f"Confirmation: {confirmation_json}")

        return confirmation_json

    def run(self):
        print(f"✅ OrderManager initialized on {self.host}:{self.port}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("✅ OrderManager stopped")
