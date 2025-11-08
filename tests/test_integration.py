import pytest
from src.strategy import Strategy

def test_strategy_integration(monkeypatch):
    """Integration test for Strategy, Gateway, and OrderManager"""

    strat = Strategy()

    # Prevent infinite loop in gateway/strategy
    monkeypatch.setattr("time.sleep", lambda x: (_ for _ in ()).throw(KeyboardInterrupt))

    try:
        strat.run()
    except KeyboardInterrupt:
        pass

    # Check that the strategy's OrderManager sent at least one order
    assert hasattr(strat, "om"), "Strategy should have an OrderManager instance"
    assert len(strat.om.sent_orders) > 0
    for order in strat.om.sent_orders:
        assert "symbol" in order
        assert "side" in order
        assert "qty" in order
        assert "price" in order
    print("✅ Integration test passed successfully")
