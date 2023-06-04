from fastapi import APIRouter, Depends
from src.interfaces.cabinet_interface import (
    CabinetInterface,
    CabinetConnectionError
)
from dependencies import (
    verify_token,
    get_database,
    get_cabinet_client,
    get_url_parameters,
    get_project_id
)
from src.interfaces.database import Database
from loguru import logger
import responses


logger.info("Module started")
router = APIRouter(
    dependencies=[Depends(verify_token)]
)
logger.info("Global variables were defined")


@router.post("/subscription")
async def create_subscription(
        project_id: int = Depends(get_project_id),
        zulip_channel_info: dict = Depends(get_url_parameters),
        db: Database = Depends(get_database),
        cabinet: CabinetInterface = Depends(get_cabinet_client)):
    if db.exists(project_id):
        logger.info(
            f"Project \"{project_id}\" was found in database, updating")
        db.update_zulip_channel(
            project_id,
            zulip_channel_info["stream"],
            zulip_channel_info["topic"]
        )
        return responses.SUCCESS_UPDATE

    try:
        cabinet_applications = await cabinet.get_all_applications(project_id)
    except CabinetConnectionError:
        logger.warning("Cabinet error occurred while getting applications.")
        return responses.CABINET_ERROR

    logger.info("Inserting project into database")
    db.insert_record(
        project_id,
        zulip_channel_info["stream"],
        zulip_channel_info["topic"],
        cabinet_applications
    )
    return responses.SUCCESS


@router.delete("/subscription")
async def delete_subscription(
        project_id: int = Depends(get_project_id),
        db: Database = Depends(get_database)):
    if not db.exists(project_id):
        logger.info(f'"{project_id}" is not subscribed')
        return responses.NOT_SUBSCRIBED

    logger.info("Deleting project from database")
    db.delete_record(project_id)
    return responses.SUCCESS_DEL
