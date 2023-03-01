import os
import sys
import logging
from dotenv import load_dotenv


load_dotenv()
formatter = logging.Formatter(
    "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
)
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(
        int(os.environ["LOG_LEVEL"]) if "LOG_LEVEL" in os.environ
        else logging.INFO
    )
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
