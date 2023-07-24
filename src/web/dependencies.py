import os
from configparser import ConfigParser
from fastapi import Header, HTTPException, status
from loguru import logger
from src.models import Project
from src.postgres.project_repository import PostgresProjectRepository
from src.postgres.application_repository import PostgresApplicationRepository
from src.container import Container
from src.clients.cabinet_client import (
    CabinetClient,
    CabinetConnectionError
)


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


async def get_project_id(slug: int) -> int:
    cabinet = Container.get(CabinetClient)
    try:
        project_id = await cabinet.get_project_id_from_slug(slug)
    except CabinetConnectionError:
        logger.warning("Cabinet error occurred while getting project id.")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=response_texts["CabinetError"]
        )
    if project_id is None:
        logger.info(f"Project with slug {slug} doesn't exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response_texts["ProjectNotFound"]
        )
    return project_id


async def get_project(slug: int, stream: str, topic: str) -> Project:
    project_id = await get_project_id(slug)
    return Project(project_id, stream, topic)


async def get_project_repo():
    return Container.get(PostgresProjectRepository)


async def get_application_repo():
    return Container.get(PostgresApplicationRepository)


async def get_cabinet_client():
    return Container.get(CabinetClient)
