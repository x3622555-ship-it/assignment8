import pytest
from src.gateway import Gateway
from src.ordermanager import OrderManager
import json

def test_gateway_price_format(monkeypatch, capsys):
    """Test that Gateway prints prices in correct format"""
    gw = Gateway()

    # Stop infinite loop
    monkeypatch.setattr("time.sleep", lambda x: (_ for _ in ()).throw(KeyboardInterrupt))

    try:
        gw.run()
    except KeyboardInterrupt:
        pass

    captured = capsys.readouterr().out
    assert "PRICE," in captured
    assert "*" in captured
    print("✅ Gateway price output format OK")

def test_ordermanager_send_order():
    """Test that OrderManager returns valid JSON confirmation"""
    om = OrderManager()
    order = {"symbol": "AAPL", "side": "BUY", "qty": 10, "price": 100.0}
    response = om.send_order(order)

    data = json.loads(response)
    assert data["status"] == "ACCEPTED"
    assert data["symbol"] == "AAPL"
    assert data["side"] == "BUY"
    assert data["qty"] == 10
    assert data["price"] == 100.0
    print("✅ OrderManager confirmation OK")
