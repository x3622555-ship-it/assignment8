from src.gateway import Gateway
from src.ordermanager import OrderManager
import time
import random
import logging

# Configure system log
system_logger = logging.getLogger("system")

class Strategy:
    def __init__(self):
        self.gateway = Gateway()
        self.om = OrderManager()

    def run(self):
        print("🚀 Strategy started...")
        system_logger.info("Strategy started")
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for _ in range(5):  # limit to 5 trading cycles
            symbol = random.choice(symbols)
            price = self.gateway.get_price(symbol)
            print(f"📊 {symbol} price: {price}")

            if price < 100:
                order = {"symbol": symbol, "side": "BUY", "qty": 10, "price": price}
            else:
                order = {"symbol": symbol, "side": "SELL", "qty": 10, "price": price}

            system_logger.info(f"Generated {order['side']} order for {symbol} at {price}")
            self.om.send_order(order)
            time.sleep(1)

        print("✅ Strategy completed.")
        system_logger.info("Strategy completed")

if __name__ == "__main__":
    strat = Strategy()
    strat.run()
