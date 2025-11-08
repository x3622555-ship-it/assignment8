# src/ordermanager.py
from src.orderbook import OrderBook

class OrderManager:
    def __init__(self):
        self.order_book = OrderBook()

    def place_order(self, symbol, price, qty):
        order = {"symbol": symbol, "price": price, "qty": qty}
        self.order_book.add_order(order)
        print(f"Order placed: {order}")

    def show_all_orders(self):
        self.order_book.show_orders()

# __main__ block for independent run
if __name__ == "__main__":
    om = OrderManager()
    om.place_order("AAPL", 150, 1)
    om.place_order("MSFT", 300, 2)
    om.show_all_orders()
