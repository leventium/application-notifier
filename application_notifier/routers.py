import responses
from interfaces import CabinetInterface
from functions import bring_to_mongo_format, get_env_variables
from fastapi import APIRouter, Request
import pymongo


env = get_env_variables()
router = APIRouter()


@router.on_event("startup")
async def start():
    global db
    global cabinet
    db = pymongo.MongoClient(env["MONGO"]).db
    cabinet = CabinetInterface(env["CABINET_URL"])


@router.on_event("shutdown")
async def stop():
    global db
    global cabinet
    db.close()
    await cabinet.close()


@router.post("/subscription/{slug}")
async def create_subscription(slug: int, request: Request):
    if request.headers["authorization"] != env["SECRET"]:
        return responses.UNAUTHORIZED

    if not cabinet.exists(slug):
        return responses.PROJECT_NOT_FOUND

    db.subscribed_projects.insert_one({"_id": slug})
    project_applications = bring_to_mongo_format(
        cabinet.get_all_applications(slug),
        slug
    )
    db.applications.insert_many(project_applications)
    return responses.SUCCESS


@router.delete("/subscription/{slug}")
async def delete_subscription(slug: int, request: Request):
    if request.headers["authorization"] != env["SECRET"]:
        return responses.UNAUTHORIZED
    
    if not cabinet.exists(slug):
        return responses.PROJECT_NOT_FOUND
    
    if len(list(db.subscribed_projects.find({"_id": slug}))) == 0:
        return responses.NOT_SUBSCRIBED
    
    db.applications.delete_many({"project_id": slug})
    db.subscribed_projects.delete_one({"_id": slug})
    return responses.SUCCESS_DEL
