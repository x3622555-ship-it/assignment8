from src.shared_memory_utils import SharedPriceBook

def test_shared_pricebook():
    """Test SharedPriceBook functionality"""
    book = SharedPriceBook()
    book.update_price("AAPL", 100.5)
    book.update_price("MSFT", 105.2)

    assert book.get_price("AAPL") == 100.5
    assert book.get_price("MSFT") == 105.2
    assert book.get_price("GOOGL") is None  # not updated
    print("✅ SharedPriceBook works correctly")
