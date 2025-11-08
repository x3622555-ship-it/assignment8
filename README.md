🏗️ Trading System Architecture
          ┌───────────────┐
          │   Gateway     │
          │ (Price Feed)  │
          └─────┬─────────┘
                │ Broadcasts Prices (PRICE,<symbol>,<price>*)
                ▼
        ┌───────────────┐
        │  OrderBook    │
        │ (Shared Memory)│
        └─────┬─────────┘
                │ Provides latest prices
                ▼
        ┌───────────────┐
        │  Strategy     │
        │ (Trading Logic│
        │  & Decisions) │
        └─────┬─────────┘
                │ Sends Orders
                ▼
        ┌───────────────┐
        │ OrderManager  │
        │ (Confirms)    │
        └───────────────┘

▶️ Run Instructions (General)

Open your terminal and navigate to the project folder.

Activate your virtual environment.

Install project dependencies if not already installed.

Start the trading system, either by:

Running each component (Gateway, OrderBook, OrderManager, Strategy) in separate terminals, or

Running the main script that launches all components together.

Observe outputs in the console or log files to monitor live prices, orders sent, and confirmations.

Stop all components safely when finished.

🧪 Run Tests (General)

Ensure the virtual environment is active.

Run the test suite for the project.

Verify that all tests pass successfully.

Stop any running modules before testing if necessary.
