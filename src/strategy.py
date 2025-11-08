# src/strategy.py
from src.gateway import Gateway
from src.ordermanager import OrderManager

class Strategy:
    def __init__(self, gateway=None, order_manager=None):
        self.gateway = gateway
        self.order_manager = order_manager

    def run(self):
        """Simple strategy: buy 1 unit of each stock if price below threshold."""
        if self.gateway is None or self.order_manager is None:
            print("No gateway or order manager assigned.")
            return

        market_data = self.gateway.get_market_data()
        for symbol, price in market_data.items():
            if symbol == "AAPL" and price < 155:
                self.order_manager.place_order(symbol, price, 1)
            elif symbol == "MSFT" and price < 310:
                self.order_manager.place_order(symbol, price, 1)
            elif symbol == "GOOG" and price < 2650:
                self.order_manager.place_order(symbol, price, 1)

# __main__ block for independent run
if __name__ == "__main__":
    gateway = Gateway("DemoGateway")
    order_manager = OrderManager()
    strategy = Strategy(gateway, order_manager)
    strategy.run()
    order_manager.show_all_orders()
