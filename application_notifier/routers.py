import os
import responses
from cabinet_interface import CabinetInterface
from functions import bring_to_mongo_format, check_env
from fastapi import APIRouter, Request
from dotenv import load_dotenv
import pymongo


load_dotenv()
check_env(
    "MONGO_CONNSTRING",
    "CABINET_URL",
    "SECRET"
)
router = APIRouter()


@router.on_event("startup")
async def start():
    global db
    global mongo
    global cabinet
    mongo = pymongo.MongoClient(os.environ["MONGO_CONNSTRING"])
    db = mongo.db
    cabinet = CabinetInterface(os.environ["CABINET_URL"])


@router.on_event("shutdown")
async def stop():
    global mongo
    global cabinet
    mongo.close()
    await cabinet.close()


@router.post("/subscription/{slug}/{stream}/{topic}")
async def create_subscription(slug: int, stream: str,
                              topic: str, request: Request):
    stream = stream.replace("_", " ")
    topic = topic.replace("_", " ")
    if request.headers["authorization"] != f"Bearer {os.environ['SECRET']}":
        return responses.UNAUTHORIZED

    if not await cabinet.exists(slug):
        return responses.PROJECT_NOT_FOUND

    if tuple(db.subscribed_projects.find({"_id": slug})):
        db.subscribed_projects.update_one(
            {"_id": slug},
            {"$set": {
                "stream": stream,
                "topic": topic
            }}
        )
        return responses.SUCCESS

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
    if request.headers["authorization"] != f"Bearer {os.environ['SECRET']}":
        return responses.UNAUTHORIZED

    if not await cabinet.exists(slug):
        return responses.PROJECT_NOT_FOUND

    if len(list(db.subscribed_projects.find({"_id": slug}))) == 0:
        return responses.NOT_SUBSCRIBED

    db.applications.delete_many({"project_id": slug})
    db.subscribed_projects.delete_one({"_id": slug})
    return responses.SUCCESS_DEL
