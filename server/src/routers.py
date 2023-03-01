import os
import responses
from get_logger import get_logger
from cabinet_interface import CabinetInterface
from formatting import bring_to_mongo_format
from fastapi import APIRouter, Request
from dotenv import load_dotenv
import pymongo


logger = get_logger(__name__)
logger.info("Module started")
load_dotenv()
router = APIRouter()
db = None
mongo = None
cabinet = None
logger.info("Global variables were defined")


@router.on_event("startup")
async def start():
    global db
    global mongo
    global cabinet
    logger.info("Including interfaces")
    mongo = pymongo.MongoClient(os.environ["MONGO_CONNSTRING"])
    db = mongo.db
    cabinet = CabinetInterface(os.environ["CABINET_URL"])
    logger.info("Interfaces were included")


@router.on_event("shutdown")
async def stop():
    global mongo
    global cabinet
    logger.info("Closing dependencies")
    mongo.close()
    await cabinet.close()
    logger.info("Dependencies were closed")


@router.post("/subscription/{slug}/{stream}/{topic}")
async def create_subscription(slug: int, stream: str,
                              topic: str, request: Request):
    logger.info(f"POST /subscription/{slug}/{stream}/{topic} received")
    stream = stream.replace("_", " ")
    topic = topic.replace("_", " ")
    try:
        if (request.headers["authorization"] !=
                f"Bearer {os.environ['SECRET']}"):
            logger.info("Unauthorized")
            return responses.UNAUTHORIZED
    except KeyError:
        logger.info("Unauthorized")
        return responses.UNAUTHORIZED

    if not await cabinet.exists(slug):
        logger.info("Doesn't exist")
        return responses.PROJECT_NOT_FOUND

    if tuple(db.subscribed_projects.find({"_id": slug})):
        logger.info("Finded in database, updating")
        db.subscribed_projects.update_one(
            {"_id": slug},
            {"$set": {
                "stream": stream,
                "topic": topic
            }}
        )
        return responses.SUCCESS

    logger.info("Inserting in database")
    db.subscribed_projects.insert_one({
        "_id": slug,
        "stream": stream,
        "topic": topic
    })
    cabinet_applications = await cabinet.get_all_applications(slug)
    project_applications = bring_to_mongo_format(cabinet_applications, slug)
    db.applications.insert_many(project_applications)
    return responses.SUCCESS


@router.delete("/subscription/{slug}")
async def delete_subscription(slug: int, request: Request):
    logger.info(f"DELETE /subscriptions/{slug}")
    try:
        if (request.headers["authorization"] !=
                f"Bearer {os.environ['SECRET']}"):
            logger.info("Unauthorized")
            return responses.UNAUTHORIZED
    except KeyError:
        logger.info("Unauthorized")
        return responses.UNAUTHORIZED

    if not await cabinet.exists(slug):
        logger.info("Doesn't exist")
        return responses.PROJECT_NOT_FOUND

    if len(list(db.subscribed_projects.find({"_id": slug}))) == 0:
        logger.info("Project not subscribed")
        return responses.NOT_SUBSCRIBED

    logger.info("Deleting")
    db.applications.delete_many({"project_id": slug})
    db.subscribed_projects.delete_one({"_id": slug})
    return responses.SUCCESS_DEL
