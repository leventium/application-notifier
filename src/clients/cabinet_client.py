import httpx
from loguru import logger
from src.models import Project, Application


class CabinetClient:
    def __init__(self, base_url):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_project_applications(
            self, project: Project) -> list[Application]:
        logger.debug(f"Getting applications for project - {project.id}.")
        try:
            res = await self.client.get(
                f"/public-api/students/project/application/{project.id}"
            )
            res.raise_for_status()
        except httpx.HTTPError:
            logger.exception(
                "Error occurred while getting new "
                f"applications for {project.id} from cabinet."
            )
            raise CabinetConnectionError(
                "Error occurred while requesting cabinet."
            )
        logger.debug(f"Applications for {project.id} were successfully got.")
        applications = []
        for app in res.json()["data"]:
            applications.append(Application(
                app["id"],
                project.id,
                app["name"],
                app["role"]
            ))
        return applications

    async def get_project_id_from_slug(self, slug: int) -> int | None:
        logger.debug(f"Getting project id for {slug}.")
        try:
            res = await self.client.get("/public-api/projects", params={
                "searchQuery": slug,
                "statusIds[]": [1, 2]
            })
            res.raise_for_status()
        except httpx.HTTPError:
            logger.exception(
                "Error occurred while getting project "
                f"id for {slug} from cabinet."
            )
            raise CabinetConnectionError(
                "Error occurred while requesting cabinet."
            )
        try:
            for project in res.json()["data"]["projects"]:
                if project["number"] == slug:
                    logger.debug(f"Id for {slug} is {project['id']}.")
                    return project["id"]
        except TypeError:
            logger.warning("Invalid JSON structure.")
            logger.warning(res.json())
        except KeyError:
            logger.warning("Invalid JSON structure.")
            logger.warning(res.json())
        return None

    async def close(self) -> None:
        await self.client.aclose()


class CabinetConnectionError(Exception):
    pass
