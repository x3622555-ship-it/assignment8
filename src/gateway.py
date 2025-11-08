import time
import random
import logging

# Configure system log
system_logger = logging.getLogger("system")
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler("system.log", mode="a")
system_formatter = logging.Formatter("%(asctime)s - %(message)s")
system_handler.setFormatter(system_formatter)
system_logger.addHandler(system_handler)

class Gateway:
    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self.price_history = []

    def get_price(self, symbol):
        price = round(random.uniform(95, 110), 2)
        self.price_history.append((symbol, price))

        # Limit to 10 most recent prices
        if len(self.price_history) > 10:
            self.price_history.pop(0)

        system_logger.info(f"{symbol} price: {price}")
        return price

    def run(self):
        print(f"✅ Gateway listening on {self.host}:{self.port}")
        try:
            while True:
                for symbol in ["AAPL", "MSFT", "GOOGL"]:
                    price = self.get_price(symbol)
                    print(f"PRICE,{symbol},{price}*")
                time.sleep(1)
        except KeyboardInterrupt:
            print("✅ Gateway stopped")
