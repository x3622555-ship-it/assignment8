import unittest
from src.gateway import Gateway
from src.orderbook import OrderBook
from src.shared_memory_utils import read_shared_memory

class TestGatewayOrderBook(unittest.TestCase):
    def setUp(self):
        self.gateway = Gateway("DemoGateway")
        self.orderbook = OrderBook()

    def test_market_data_updates_shared_memory(self):
        market_data = self.gateway.get_market_data()
        shared_data = read_shared_memory()
        self.assertEqual(market_data, shared_data)

    def test_orderbook_add_order(self):
        order = {"symbol": "AAPL", "price": 150, "qty": 10}
        self.orderbook.add_order(order)
        shared_orders = read_shared_memory()
        self.assertIn(order, shared_orders)

if __name__ == "__main__":
    unittest.main()
