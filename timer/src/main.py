import os
import time
import asyncio
import pymongo
import zulip
from dotenv import load_dotenv
from get_logger import get_logger
from formatting import bring_to_mongo_format
from cabinet_interface import CabinetInterface


load_dotenv()
logger = get_logger(__name__)
MSG_TEXT = """\
От **{}** была подана заявка на вакансию **{}**\
"""


async def check_new_applications():
    logger.info("New applications check process is starting")
    for project in tuple(db.subscribed_projects.find()):
        logger.info(f"Checking project: {project['_id']}")
        cabinet_applications = await cabinet.get_all_applications(
            project["_id"]
        )
        logger.debug("Applications were got")
        current_applications = bring_to_mongo_format(
            cabinet_applications,
            project["_id"]
        )
        logger.debug("Applications list were formatted")
        previous_applications = list(
            db.applications.find({"project_id": project["_id"]})
        )
        logger.debug("Checking applications")
        if len(current_applications) != len(previous_applications):
            logger.info(f"New applications were found for {project['_id']}")
            new_applications = [
                app for app in current_applications
                if app not in previous_applications
            ]
            for app in new_applications:
                logger.debug("Sending message")
                zulip_client.send_message({
                    "type": "stream",
                    "to": project["stream"],
                    "topic": project["topic"],
                    "content": MSG_TEXT.format(
                        app["name"],
                        app["role"].replace("/ ", " ")
                    )
                })
            logger.debug("Refreshing database")
            db.applications.insert_many(new_applications)


async def main():
    global mongo
    global db
    global zulip_client
    global cabinet
    logger.debug("Defining interfaces")
    mongo = pymongo.MongoClient(os.environ["MONGO_CONNSTRING"])
    db = mongo.db
    zulip_client = zulip.Client(
        site=os.environ["ZULIP_URL"],
        email=os.environ["BOT_EMAIL"],
        api_key=os.environ["BOT_TOKEN"]
    )
    cabinet = CabinetInterface(os.environ["CABINET_URL"])
    logger.debug("Interfaces defined")
    try:
        logger.debug("Entering cycle")
        while True:
            logger.debug("Going to function")
            await check_new_applications()
            time.sleep(int(os.getenv("COOLDOWN", "3600")))
    finally:
        await cabinet.close()
        mongo.close()


if __name__ == "__main__":
    logger.info("Timer service started")
    asyncio.run(main())
