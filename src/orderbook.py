# src/orderbook.py
from src.shared_memory_utils import update_shared_memory, read_shared_memory
from src.trades import record_trade

class OrderBook:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
        update_shared_memory(self.orders)
        record_trade(order)

    def show_orders(self):
        current_orders = read_shared_memory()
        print("Current Orders:", current_orders)

# __main__ block for independent run
if __name__ == "__main__":
    ob = OrderBook()
    ob.add_order({"symbol": "AAPL", "price": 150, "qty": 1})
    ob.add_order({"symbol": "MSFT", "price": 300, "qty": 2})
    ob.show_orders()
