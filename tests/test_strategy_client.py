import unittest
from src.strategy import Strategy
from src.gateway import Gateway
from src.ordermanager import OrderManager
from src.shared_memory_utils import read_shared_memory

class TestStrategyClient(unittest.TestCase):
    def setUp(self):
        self.gateway = Gateway("DemoGateway")
        self.order_manager = OrderManager()
        self.strategy = Strategy(self.gateway, self.order_manager)

    def test_strategy_runs_and_places_orders(self):
        self.strategy.run()
        orders = read_shared_memory()
        self.assertTrue(len(orders) > 0)
        for order in orders:
            self.assertIn("symbol", order)
            self.assertIn("price", order)
            self.assertIn("qty", order)

if __name__ == "__main__":
    unittest.main()
