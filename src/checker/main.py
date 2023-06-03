import os
import time
import asyncio
from dotenv import load_dotenv
from get_logger import get_logger
from formatting import bring_to_mongo_format
from src.interfaces.cabinet_interface import (
    CabinetInterface,
    CabinetConnectionError
)
from src.interfaces.zulip_interface import ZulipInterface
from src.interfaces.database import Database


load_dotenv()
logger = get_logger(__name__)
MSG_TEXT = """\
От **{}** была подана заявка на вакансию **{}**\
"""


async def check_new_applications():
    logger.info("New applications check process is starting")
    db = Database(os.environ["MONGO_CONNSTRING"])
    zulip_client = ZulipInterface(
        site=os.environ["ZULIP_URL"],
        email=os.environ["BOT_EMAIL"],
        api_key=os.environ["BOT_TOKEN"])
    cabinet = CabinetInterface(os.environ["CABINET_URL"])
    for project in db.get_subscribed_projects():
        logger.info(f"Checking project: {project['_id']}")
        try:
            cabinet_applications = await cabinet.get_all_applications(
                project["_id"]
            )
        except CabinetConnectionError:
            logger.warning(f"Failed to check project {project['_id']}")
            continue
        logger.debug("Applications were got")
        current_applications = bring_to_mongo_format(
            cabinet_applications,
            project["_id"]
        )
        logger.debug("Applications list were formatted")
        previous_applications = db.get_all_applications(project["_id"])
        logger.debug("Checking applications")
        if len(current_applications) != len(previous_applications):
            logger.info(f"New applications were found for {project['_id']}")
            new_applications = [
                app for app in current_applications
                if app not in previous_applications
            ]
            if len(new_applications) == 0:
                continue
            for app in new_applications:
                logger.info(f"New application from \"{app['name']}\" "
                            f"to vacancy \"{app['role']}\"")
                await zulip_client.send_message({
                    "type": "stream",
                    "to": project["stream"],
                    "topic": project["topic"],
                    "content": MSG_TEXT.format(
                        app["name"],
                        app["role"].replace("/ ", " ")
                    )
                })
            logger.debug("Refreshing database")
            db.insert_application(new_applications)
    db.close()
    await zulip_client.close()
    await cabinet.close()


async def main():
    while True:
        logger.debug("Going to function")
        await check_new_applications()
        time.sleep(int(os.getenv("COOLDOWN", "3600")))


if __name__ == "__main__":
    logger.info("Timer service started")
    asyncio.run(main())
