import unittest
from src.gateway import Gateway
from src.ordermanager import OrderManager
from src.strategy import Strategy
from src.shared_memory_utils import read_shared_memory

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.gateway = Gateway("DemoGateway")
        self.order_manager = OrderManager()
        self.strategy = Strategy(self.gateway, self.order_manager)

    def test_full_flow(self):
        # Simulate multiple market ticks
        for _ in range(2):
            market_data = self.gateway.get_market_data()
            self.strategy.run()

        orders = read_shared_memory()
        self.assertTrue(len(orders) > 0)
        for order in orders:
            self.assertIn("symbol", order)
            self.assertIn("price", order)
            self.assertIn("qty", order)

if __name__ == "__main__":
    unittest.main()
