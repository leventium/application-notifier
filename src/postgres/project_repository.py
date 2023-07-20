from src.interfaces.repositories import IProjectRepository
from postgres_queries import PostgresQueries
from src.models.project import Project


class PostgresProjectRepository(PostgresQueries, IProjectRepository):
    def __init__(self, host, port, user, password, db):
        super().__init__(host, port, user, password, db)

    async def save(self, project: Project) -> None:
        await self._execute("""
            insert into projects (id, stream, topic) values
                ($1, $2, $3)
            on conflict (id) do update set
                stream = $2,
                topic = $3;
        """, project.id, project.zulip_stream, project.zulip_topic)

    async def get_by_id(self, project_id: int) -> Project | None:
        res = await self._fetch_row("""
            select id, stream, topic
            from projects
            where id = $1;
        """, project_id)
        if res is None:
            return None
        return Project(res["id"], res["stream"], res["topic"])

    async def delete(self, project: Project) -> None:
        await self._execute("""
            delete
            from projects
            where id = $1
        """, project.id)
