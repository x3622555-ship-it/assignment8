import unittest
from src.shared_memory_utils import update_shared_memory, read_shared_memory

class TestSharedMemory(unittest.TestCase):
    def test_update_and_read(self):
        data = [{"symbol": "AAPL", "price": 150, "qty": 10}]
        update_shared_memory(data)
        self.assertEqual(read_shared_memory(), data)

    def test_overwrite_shared_memory(self):
        update_shared_memory([{"symbol": "MSFT", "price": 300, "qty": 5}])
        self.assertEqual(read_shared_memory(), [{"symbol": "MSFT", "price": 300, "qty": 5}])

if __name__ == "__main__":
    unittest.main()
