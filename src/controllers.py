from loguru import logger
from clients.cabinet_client import CabinetClient, CabinetConnectionError
from src.repositories import IProjectRepository, IApplicationRepository
from src.models import Project


class Controller:
    def __init__(
            self,
            cabinet: CabinetClient,
            project_repo: IProjectRepository,
            app_repo: IApplicationRepository
    ):
        self.cabinet = cabinet
        self.project_repo = project_repo
        self.app_repo = app_repo

    async def _get_id_from_slug(self, slug: int) -> int:
        try:
            project_id = await self.cabinet.get_project_id_from_slug(slug)
        except CabinetConnectionError:
            logger.warning("Cabinet error occurred while getting project id.")
            raise CabinetError()
        if project_id is None:
            logger.info(f"Project with slug {slug} doesn't exist.")
            raise ProjectNotFound()
        return project_id

    async def create_subscription(
            self,
            slug: int,
            zulip_stream: str,
            zulip_topic: str
    ):
        inbound_project = Project(
            await self._get_id_from_slug(slug),
            zulip_stream,
            zulip_topic
        )
        if await self.project_repo.get_by_id(inbound_project.id) is not None:
            logger.info(f"Project '{inbound_project.id}' was "
                        "found in database, updating")
            await self.project_repo.save(inbound_project)
            raise ProjectFoundAndUpdated()

        try:
            project_applications = await self.cabinet.get_project_applications(
                inbound_project
            )
        except CabinetConnectionError:
            raise CabinetError()

        logger.info("Inserting project into database")
        await self.project_repo.save(inbound_project)
        for app in project_applications:
            await self.app_repo.save(app)

    async def delete_subscription(self, slug: int):
        project_id = await self._get_id_from_slug(slug)
        if await self.project_repo.get_by_id(project_id) is None:
            logger.info(f'"{project_id}" is not subscribed')
            raise ProjectNotFound()

        logger.info("Deleting project from database")
        await self.project_repo.delete(project_id)


class CabinetError(Exception):
    pass


class ProjectNotFound(Exception):
    pass


class ProjectFoundAndUpdated(Exception):
    pass
