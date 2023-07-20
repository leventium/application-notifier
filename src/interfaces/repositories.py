"""
Module providing interfaces for database repositories.
"""
from src.models.project import Project
from src.models.application import Application


class IProjectRepository:
    async def save(self, project: Project) -> None:
        pass

    async def get_by_id(self, project_id: int) -> Project | None:
        pass

    async def get_all(self) -> list[Project]:
        pass

    async def delete(self, project_id: int) -> None:
        pass


class IApplicationRepository:
    async def save(self, app: Application) -> None:
        pass

    async def get_by_id(self, app_id: int) -> Application | None:
        pass

    async def get_by_project_id(self, project_id: int) -> list[Application]:
        pass
