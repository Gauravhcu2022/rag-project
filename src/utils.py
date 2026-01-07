import os
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def ensure_directory_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")