from dotenv import load_dotenv
from loguru import logger


load_dotenv()
logger.add("logs/logs.log", rotation="100 MB", level="INFO")
logger.add("logs/error.log", rotation="100 MB", level="ERROR")
