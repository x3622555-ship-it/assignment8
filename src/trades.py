# src/trades.py
import logging
import os

# Create logs folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def record_trade(order):
    """Record executed trade in log file."""
    logging.info(f"Trade executed: {order}")
