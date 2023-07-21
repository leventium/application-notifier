import os
import asyncio
import time
from loguru import logger
from src.interfaces.cabinet_interface import (
    CabinetInterface,
    CabinetConnectionError
)
from src.interfaces.zulip_interface import ZulipInterface
from src.service.application_service import ApplicationService
from src.postgres.application_repository import PostgresApplicationRepository
from src.postgres.project_repository import PostgresProjectRepository


MSG_TEXT = """\
От **{}** была подана заявка на вакансию **{}**\
"""


async def check_new_applications():
    logger.info("Checking for new applications")
    zulip = ZulipInterface()
    cabinet = CabinetInterface()
    project_repo = PostgresProjectRepository()
    app_repo = PostgresApplicationRepository()

    current_projects = await project_repo.get_all()
    for project in current_projects:
        logger.info(f"Checking project {project.id}")
        try:
            new_apps = await cabinet.get_project_applications(project)
        except CabinetConnectionError:
            logger.warning("Cabinet error occurred while fetching apps "
                           f"for project '{project.id}'... skipping")
            continue
        curr_apps = await app_repo.get_by_project_id(project.id)
        unique_apps = ApplicationService.find_new_applications(new_apps,
                                                               curr_apps)
        for app in unique_apps:
            logger.info(f"New app for project '{project.id}' "
                        f"- {app.user_name} | {app.role}")
            await zulip.send_message({
                "type": "stream",
                "to": project.zulip_stream,
                "topic": project.zulip_topic,
                "content": MSG_TEXT.format(
                    app.user_name,
                    app.role.replace("/ ", " ")
                )
            })
            await app_repo.save(app)

    await zulip.close()
    await cabinet.close()


async def main_loop():
    while True:
        await check_new_applications()
        time.sleep(3600 * int(os.getenv("COOLDOWN", "1")))


def main():
    logger.info("Checker service started")
    asyncio.run(main_loop())
