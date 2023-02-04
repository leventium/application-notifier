import httpx


class CabinetInterface:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_all_applications(self, project_id: int) -> list[dict]:
        res = await self.client.get(
            f"/public-api/students/project/application/{project_id}"
        )
        applications = []
        for elem in res.json()["data"]:
            new_app = {}
            new_app["id"] = elem["id"]
            new_app["userId"] = elem["userId"]
            new_app["name"] = elem["name"]
            new_app["role"] = elem["role"]
            applications.append(new_app)
        return applications

    async def exists(self, project_id: int) -> bool:
        res = await self.client.get(f"/public-api/project/header/{project_id}")
        if res.json()["code"] == 20000:
            return True
        return False

    async def close(self):
        await self.client.aclose()
