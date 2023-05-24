import os
from configparser import ConfigParser
from fastapi import Header, HTTPException, status
from cabinet_interface import CabinetInterface, CabinetConnectionError
from database import Database
from get_logger import get_logger


logger = get_logger(__name__)
config = ConfigParser()
config.read("response_texts.conf")
response_texts = config["response.texts"]


async def verify_token(authorization: str = Header(default=None)):
    if authorization is None:
        logger.debug("No token given.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response_texts["NoToken"]
        )
    logger.debug(f"Received token -- {authorization}")
    if authorization != f"Bearer {os.environ['SECRET']}":
        logger.debug("Token is wrong.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response_texts["WrongToken"]
        )


async def get_database():
    db = Database(os.environ["MONGO_CONNSTRING"])
    try:
        yield db
    finally:
        db.close()


async def get_cabinet_client():
    client = CabinetInterface(os.environ["CABINET_URL"])
    try:
        yield client
    finally:
        await client.close()


async def get_url_parameters(stream: str, topic: str):
    return {
        "stream": stream.replace("_", " "),
        "topic": topic.replace("_", " ")
    }


async def get_project_id(slug: int):
    cabinet = CabinetInterface(os.environ["CABINET_URL"])
    try:
        project_id = await cabinet.get_project_id_from_slug(slug)
    except CabinetConnectionError:
        logger.warning("Cabinet error occurred while getting project id.")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=response_texts["CabinetError"]
        )
    finally:
        await cabinet.close()
    if project_id is None:
        logger.info(f"Project with slug {slug} doesn't exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response_texts["ProjectNotFound"]
        )
    return project_id
