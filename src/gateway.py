# src/gateway.py
import random
from src.shared_memory_utils import update_shared_memory

class Gateway:
    def __init__(self, name):
        self.name = name

    def get_market_data(self):
        """Simulate fetching market prices."""
        market_data = {
            "AAPL": round(random.uniform(140, 160), 2),
            "MSFT": round(random.uniform(280, 320), 2),
            "GOOG": round(random.uniform(2500, 2700), 2)
        }
        update_shared_memory(market_data)
        return market_data

# __main__ block for independent run
if __name__ == "__main__":
    gw = Gateway("DemoGateway")
    data = gw.get_market_data()
    print("Market Data:", data)
