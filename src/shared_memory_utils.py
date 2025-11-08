# src/shared_memory_utils.py
_shared_memory = []

def update_shared_memory(data):
    """Update shared memory with new data."""
    global _shared_memory
    _shared_memory = data

def read_shared_memory():
    """Read current shared memory."""
    return _shared_memory
