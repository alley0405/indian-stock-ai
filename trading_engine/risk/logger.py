import logging
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_trade(message):
    logging.info(message)
