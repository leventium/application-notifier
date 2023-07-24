from loguru import logger
from src.service.application_service import ApplicationService
from src.interfaces.zulip_interface import ZulipInterface
from src.interfaces.cabinet_interface import (
    CabinetInterface,
    CabinetConnectionError
)
from src.interfaces.repositories import (
    IApplicationRepository,
    IProjectRepository
)


MSG_TEXT = """\
От **{}** была подана заявка на вакансию **{}**\
"""


class Checker:
    def __init__(
            self,
            zulip: ZulipInterface,
            cabinet: CabinetInterface,
            project_repo: IProjectRepository,
            app_repo: IApplicationRepository
    ):
        self.zulip = zulip
        self.cabinet = cabinet
        self.project_repo = project_repo
        self.app_repo = app_repo

    async def check_new_applications(self):
        current_projects = await self.project_repo.get_all()
        for project in current_projects:
            logger.info(f"Checking project {project.id}")
            try:
                new_apps = await self.cabinet.get_project_applications(project)
            except CabinetConnectionError:
                logger.warning("Cabinet error occurred while fetching apps "
                               f"for project '{project.id}'... skipping")
                continue
            curr_apps = await self.app_repo.get_by_project_id(project.id)
            unique_apps = ApplicationService.find_new_applications(new_apps,
                                                                   curr_apps)
            for app in unique_apps:
                logger.info(f"New app for project '{project.id}' "
                            f"- {app.user_name} | {app.role}")
                await self.zulip.send_message(dict(
                    type="stream",
                    to=project.zulip_stream,
                    topic=project.zulip_topic,
                    content=MSG_TEXT.format(
                        app.user_name,
                        app.role.replace("/ ", " ")
                    )))
                await self.app_repo.save(app)
