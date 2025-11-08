import time
from .shared_memory_utils import update_shared_memory, read_shared_memory

class OrderBook:
    def __init__(self):
        self.stocks = ["AAPL", "MSFT", "GOOGL"]

    def run(self):
        print(f"📡 OrderBook running")
        try:
            while True:
                for stock in self.stocks:
                    # Simulate receiving price from Gateway
                    price = round(read_shared_memory(stock) or 100, 2)
                    update_shared_memory(stock, price)
                    print(f"💾 Updated shared memory for {stock}: {price}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("✅ OrderBook stopped")
