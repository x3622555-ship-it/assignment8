# main.py
from src.gateway import Gateway
from src.ordermanager import OrderManager
from src.strategy import Strategy

def main():
    gateway = Gateway("DemoGateway")
    order_manager = OrderManager()
    strategy = Strategy(gateway, order_manager)

    # Simulate market ticks
    for _ in range(3):
        market_data = gateway.get_market_data()
        print("Market Data:", market_data)
        strategy.run()

    order_manager.show_all_orders()

if __name__ == "__main__":
    main()
