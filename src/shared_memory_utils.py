# shared_memory_utils.py

import threading

class SharedPriceBook:
    """
    Thread-safe shared memory price book for storing stock prices.
    Can be used by OrderBook and Strategy for real-time access.
    """

    def __init__(self):
        self._prices = {}
        self._lock = threading.Lock()

    def update_price(self, symbol: str, price: float):
        """Update the price of a stock"""
        with self._lock:
            self._prices[symbol] = price
            # Optional: print for debugging
            # print(f"💾 Updated shared memory for {symbol}: {price}")

    def get_price(self, symbol: str):
        """Get the latest price of a stock"""
        with self._lock:
            return self._prices.get(symbol, None)

    def get_all_prices(self):
        """Get a copy of all stock prices"""
        with self._lock:
            return self._prices.copy()
