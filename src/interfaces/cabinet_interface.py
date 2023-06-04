import httpx
from loguru import logger


class CabinetInterface:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_all_applications(self, project_id: int) -> list[dict]:
        logger.debug(f"Getting applications for {project_id}.")
        try:
            res = await self.client.get(
                f"/public-api/students/project/application/{project_id}"
            )
        except httpx.TimeoutException:
            logger.exception(
                "Error occurred while getting new "
                f"applications for {project_id} from cabinet."
            )
            raise CabinetConnectionError(
                "Timeout limit exited while requesting cabinet."
            )
        logger.debug(f"Applications for {project_id} were successfully got.")
        applications = []
        for elem in res.json()["data"]:
            new_app = {
                "id": elem["id"],
                "userId": elem["userId"],
                "name": elem["name"],
                "role": elem["role"]
            }
            applications.append(new_app)
        return applications

    async def get_project_id_from_slug(self, slug: int) -> int | None:
        logger.debug(f"Getting project id for {slug}.")
        try:
            res = await self.client.get("/public-api/projects", params={
                "searchQuery": slug,
                "statusIds[]": 2
            })
        except httpx.TimeoutException:
            logger.exception(
                "Error occurred while getting project "
                f"id for {slug} from cabinet."
            )
            raise CabinetConnectionError(
                "Timeout limit exited while requesting cabinet."
            )
        try:
            for project in res.json()["data"]["projects"]:
                if project["number"] == slug:
                    logger.debug(f"Id for {slug} is {project['id']}.")
                    return project["id"]
        except TypeError:
            logger.warning("Invalid JSON structure.")
            logger.debug(res.json())
        except KeyError:
            logger.warning("Invalid JSON structure.")
            logger.debug(res.json())
        return None

    async def close(self) -> None:
        await self.client.aclose()


class CabinetConnectionError(Exception):
    pass
