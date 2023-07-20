from fastapi import APIRouter, Depends
from loguru import logger
from src.interfaces.cabinet_interface import (
    CabinetInterface,
    CabinetConnectionError
)
from src.models.project import Project
from dependencies import (
    verify_token,
    get_project_id,
    get_project,
    get_project_repo,
    get_application_repo
)
from src.interfaces.repositories import (
    IApplicationRepository,
    IProjectRepository
)
import responses


router = APIRouter(
    dependencies=[Depends(verify_token)]
)


@router.post("/subscription")
async def create_subscription(
        received_project: Project = Depends(get_project),
        project_repo: IProjectRepository = Depends(get_project_repo),
        application_repo: IApplicationRepository = Depends(get_application_repo)
        ):
    if await project_repo.get_by_id(received_project.id) is not None:
        logger.info(f"Project '{received_project.id}' was found in database, "
                    "updating")
        await project_repo.save(received_project)
        return responses.SUCCESS_UPDATE

    try:
        cabinet = CabinetInterface()
        project_applications = await cabinet.get_project_applications(
            received_project
        )
    except CabinetConnectionError:
        return responses.CABINET_ERROR

    logger.info("Inserting project into database")
    await project_repo.save(received_project)
    for app in project_applications:
        await application_repo.save(app)
    return responses.SUCCESS


@router.delete("/subscription")
async def delete_subscription(
        project_id: int = Depends(get_project_id),
        project_repo: IProjectRepository = Depends(get_project_repo)):
    if await project_repo.get_by_id(project_id) is None:
        logger.info(f'"{project_id}" is not subscribed')
        return responses.NOT_SUBSCRIBED

    logger.info("Deleting project from database")
    await project_repo.delete(project_id)
    return responses.SUCCESS_DEL
