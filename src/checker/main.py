import os
import asyncio
import time
from loguru import logger
from checker import Checker


async def main_loop(checker: Checker):
    while True:
        await checker.check_new_applications()
        time.sleep(3600 * int(os.getenv("COOLDOWN", "1")))


def main(checker: Checker):
    logger.info("Checker service started")
    asyncio.run(main_loop(checker))
