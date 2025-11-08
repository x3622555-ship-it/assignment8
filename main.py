import threading
import time
from src.gateway import Gateway
from src.orderbook import OrderBook
from src.ordermanager import OrderManager
from src.strategy import Strategy

def run_gateway():
    Gateway().run()

def run_orderbook():
    OrderBook().run()

def run_ordermanager():
    OrderManager().run()

def run_strategy():
    strat = Strategy()
    strat.connect_gateway()
    strat.connect_ordermanager()
    strat.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run_gateway, name="GatewayThread"),
        threading.Thread(target=run_orderbook, name="OrderBookThread"),
        threading.Thread(target=run_ordermanager, name="OrderManagerThread"),
        threading.Thread(target=run_strategy, name="StrategyThread")
    ]

    for t in threads:
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()
