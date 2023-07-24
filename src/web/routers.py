from fastapi import APIRouter, Depends
from src.container import Container
from src.controllers import (
    Controller,
    CabinetError,
    ProjectNotFound,
    ProjectFoundAndUpdated
)
from dependencies import verify_token
import responses


router = APIRouter(
    dependencies=[Depends(verify_token)]
)


@router.post("/subscription")
async def create_subscription(slug: int, zulip_stream: str, zulip_topic: str):
    controller = Container.get(Controller)
    try:
        controller.create_subscription(slug, zulip_stream, zulip_topic)
    except CabinetError:
        return responses.CABINET_ERROR
    except ProjectNotFound:
        return responses.PROJECT_NOT_FOUND
    except ProjectFoundAndUpdated:
        return responses.SUCCESS_UPDATE
    return responses.SUCCESS


@router.delete("/subscription")
async def delete_subscription(slug: int):
    controller = Container.get(Controller)
    try:
        controller.delete_subscription(slug)
    except ProjectNotFound:
        return responses.NOT_SUBSCRIBED
    return responses.SUCCESS_DEL
