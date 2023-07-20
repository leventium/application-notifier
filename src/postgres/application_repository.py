from src.interfaces.repositories import IApplicationRepository
from postgres_queries import PostgresQueries
from src.models.application import Application


class PostgresApplicationRepository(PostgresQueries, IApplicationRepository):
    async def save(self, app: Application) -> None:
        await self._execute("""
            insert into applications (id, name, role, project_id) values
                ($1, $2, $3, $4)
            on conflict (id) do update set
                name = $2,
                role = $3,
                project_id = $4;
        """, app.id, app.user_name, app.role, app.project_id)

    async def get_by_id(self, app_id: int) -> Application | None:
        res = await self._fetch_row("""
            select id, name, role, project_id
            from applications
            where id = $1;
        """, app_id)
        if res is None:
            return None
        return Application(
            res["id"],
            res["project_id"],
            res["name"],
            res["role"]
        )

    async def get_by_project_id(self, project_id: int) -> list[Application]:
        res = await self._fetch("""
            select id, name, role, project_id
            from applications
            where project_id = $1;
        """, project_id)
        return [Application(
            elem["id"],
            elem["project_id"],
            elem["name"],
            elem["role"]
        ) for elem in res]
