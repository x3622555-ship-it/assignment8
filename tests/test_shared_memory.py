# tests/test_shared_memory.py
import multiprocessing as mp
import time
from src.shared_memory_utils import SharedPriceBook

SYMS = ["AAPL", "MSFT", "GOOG"]

def writer_process(names):
    try:
        spb = SharedPriceBook(symbols=SYMS, name_prefix=names["prefix"], existing=True)
        time.sleep(0.5)  # small delay to ensure memory ready
        spb.update("AAPL", 100.5)
        spb.update("MSFT", 200.75)
        spb.close()
    except Exception as e:
        print("Writer error:", e)

def reader_process(names, result_queue):
    try:
        spb = SharedPriceBook(symbols=SYMS, name_prefix=names["prefix"], existing=True)
        time.sleep(1.0)
        data = spb.read_all()
        result_queue.put(data)
        spb.close()
    except Exception as e:
        print("Reader error:", e)

def test_shared_memory_roundtrip():
    spb = SharedPriceBook(symbols=SYMS, name_prefix="test_spb", existing=False)
    names = {"prefix": "test_spb"}
    q = mp.Queue()
    p_writer = mp.Process(target=writer_process, args=(names,))
    p_reader = mp.Process(target=reader_process, args=(names, q))
    p_writer.start()
    p_reader.start()
    p_writer.join()
    p_reader.join(timeout=5)

    assert p_reader.exitcode == 0, "Reader process crashed"
    assert not q.empty(), "Reader did not put data in queue"
    result = q.get(timeout=5)

    spb.close()
    spb.unlink()
    assert result["AAPL"] == 100.5
    assert result["MSFT"] == 200.75
    assert result["GOOG"] is None
