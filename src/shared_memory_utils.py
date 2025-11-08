# src/shared_memory_utils.py
"""
SharedPriceBook
---------------
A simple shared-memory class that allows multiple processes
to share and update stock prices safely.

Features:
- Uses Python's multiprocessing.shared_memory
- Stores a fixed list of symbols and their latest prices
- Supports atomic read/write using a multiprocessing.Lock
- Allows multiple processes to attach using a shared name prefix
"""

import numpy as np
from multiprocessing import shared_memory, Lock
import json
import time


class SharedPriceBook:
    HEADER_NAME_SUFFIX = "_spb_header"
    PRICES_NAME_SUFFIX = "_spb_prices"

    def __init__(self, symbols, name_prefix=None, existing=False, lock=None):
        """
        Initialize or attach to a shared memory price book.

        Args:
            symbols (list[str]): Stock symbols to track (e.g., ["AAPL", "MSFT"])
            name_prefix (str): Prefix to identify the shared memory blocks
            existing (bool): True to attach to existing shared memory segments
            lock (Lock): Optional multiprocessing.Lock shared across processes
        """
        self.symbols = list(symbols)
        self.n = len(self.symbols)
        self.lock = lock or Lock()

        prefix = name_prefix or f"spb_{int(time.time() * 1000)}"
        self.header_name = prefix + self.HEADER_NAME_SUFFIX
        self.prices_name = prefix + self.PRICES_NAME_SUFFIX

        if existing:
            self._attach_existing()
        else:
            self._create_new()

    # ----------------------------------------------------------
    # Create new shared memory segments
    # ----------------------------------------------------------
    def _create_new(self):
        # Mapping symbol -> index
        mapping = {sym: i for i, sym in enumerate(self.symbols)}
        header_bytes = json.dumps(mapping).encode("utf-8")

        header_size = 1024  # 1 KB header
        if len(header_bytes) > header_size:
            raise ValueError("Header too large (too many or too long symbols).")

        # Create header shared memory
        self.header_shm = shared_memory.SharedMemory(
            create=True, size=header_size, name=self.header_name
        )

        # Write header JSON into buffer
        self.header_shm.buf[: len(header_bytes)] = header_bytes
        for i in range(len(header_bytes), header_size):
            self.header_shm.buf[i] = 0

        # Create price array shared memory
        dtype = np.float64
        self.prices_nbytes = self.n * np.dtype(dtype).itemsize
        self.prices_shm = shared_memory.SharedMemory(
            create=True, size=self.prices_nbytes, name=self.prices_name
        )

        # Initialize all prices to NaN
        arr = np.ndarray((self.n,), dtype=dtype, buffer=self.prices_shm.buf)
        arr[:] = np.nan

        self._mapping = mapping

    # ----------------------------------------------------------
    # Attach to existing shared memory
    # ----------------------------------------------------------
    def _attach_existing(self):
        # Attach to header
        self.header_shm = shared_memory.SharedMemory(name=self.header_name)
        raw = bytes(self.header_shm.buf).split(b"\x00", 1)[0]
        mapping = json.loads(raw.decode("utf-8"))
        self._mapping = mapping

        # Attach to prices
        dtype = np.float64
        self.prices_nbytes = len(mapping) * np.dtype(dtype).itemsize
        self.prices_shm = shared_memory.SharedMemory(name=self.prices_name)

        # Restore symbols list
        self.n = len(mapping)
        self.symbols = [None] * self.n
        for sym, idx in mapping.items():
            self.symbols[idx] = sym

    # ----------------------------------------------------------
    # Core methods
    # ----------------------------------------------------------
    def update(self, symbol, price):
        """Update a symbol's price atomically."""
        if symbol not in self._mapping:
            raise KeyError(f"Unknown symbol: {symbol}")
        idx = self._mapping[symbol]
        with self.lock:
            arr = np.ndarray((self.n,), dtype=np.float64, buffer=self.prices_shm.buf)
            arr[idx] = float(price)

    def read(self, symbol):
        """Read the latest price for one symbol."""
        if symbol not in self._mapping:
            raise KeyError(f"Unknown symbol: {symbol}")
        idx = self._mapping[symbol]
        with self.lock:
            arr = np.ndarray((self.n,), dtype=np.float64, buffer=self.prices_shm.buf)
            val = arr[idx]
            return None if np.isnan(val) else float(val)

    def read_all(self):
        """Return all symbol prices as a dictionary."""
        with self.lock:
            arr = np.ndarray((self.n,), dtype=np.float64, buffer=self.prices_shm.buf)
            result = {
                self.symbols[i]: (None if np.isnan(arr[i]) else float(arr[i]))
                for i in range(self.n)
            }
        return result

    # ----------------------------------------------------------
    # Cleanup
    # ----------------------------------------------------------
    def close(self):
        """Close the shared memory blocks (does not unlink)."""
        try:
            self.prices_shm.close()
        except Exception:
            pass
        try:
            self.header_shm.close()
        except Exception:
            pass

    def unlink(self):
        """Unlink (destroy) shared memory blocks when done."""
        try:
            self.prices_shm.unlink()
        except Exception:
            pass
        try:
            self.header_shm.unlink()
        except Exception:
            pass

    def names(self):
        """Return the shared memory block names (useful for debugging)."""
        return {"header": self.header_name, "prices": self.prices_name}
