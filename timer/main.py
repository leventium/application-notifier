import os
import time
import asyncio
from functions import check_env, bring_to_mongo_format
from cabinet_interface import CabinetInterface
import pymongo
import zulip
from dotenv import load_dotenv


load_dotenv()
check_env(
    "MONGO_CONNSTRING",
    "ZULIP_URL",
    "BOT_EMAIL",
    "BOT_TOKEN",
    "CABINET_URL"
)

MSG_TEXT = """\
От **{}** была подана заявка на вакансию **{}**\
"""


async def check_new_applications():
    for project in tuple(db.subscribed_projects.find()):
        cabinet_applications = await cabinet.get_all_applications(
            project["_id"]
        )
        current_applications = bring_to_mongo_format(
            cabinet_applications,
            project["_id"]
        )
        previous_applications = list(
            db.applications.find({"project_id": project["_id"]})
        )
        if len(current_applications) != len(previous_applications):
            new_applications = [
                app for app in current_applications
                if app not in previous_applications  # TODO make application status checks
            ]
            for app in new_applications:
                zulip_client.send_message({
                    "type": "stream",
                    "to": project["stream"],
                    "topic": project["topic"],
                    "content": MSG_TEXT.format(app["name"], app["role"])
                })
            db.applications.insert_many(new_applications)


async def main():
    global mongo
    global db
    global zulip_client
    global cabinet
    mongo = pymongo.MongoClient()
    db = mongo.db
    zulip_client = zulip.Client(
        site=os.environ["ZULIP_URL"],
        email=os.environ["BOT_EMAIL"],
        api_key=os.environ["BOT_TOKEN"]
    )
    cabinet = CabinetInterface(os.environ["CABINET_URL"])
    try:
        while True:
            await check_new_applications()
            time.sleep(3600)
    except:
        pass
    finally:
        await cabinet.close()
        mongo.close()


if __name__ == "__main__":
    asyncio.run(main())
