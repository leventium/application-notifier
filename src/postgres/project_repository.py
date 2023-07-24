from asyncpg import pool
from src.interfaces.repositories import IProjectRepository
from src.models import Project


class PostgresProjectRepository(IProjectRepository):
    def __init__(self, pool: pool):
        self.pool = pool

    async def save(self, project: Project) -> None:
        await self.pool.execute("""
            insert into projects (id, stream, topic) values
                ($1, $2, $3)
            on conflict (id) do update set
                stream = $2,
                topic = $3;
        """, project.id, project.zulip_stream, project.zulip_topic)

    async def get_by_id(self, project_id: int) -> Project | None:
        res = await self.pool.fetchrow("""
            select id, stream, topic
            from projects
            where id = $1;
        """, project_id)
        if res is None:
            return None
        return Project(res["id"], res["stream"], res["topic"])

    async def get_all(self) -> list[Project]:
        res = await self.pool.fetch("""
            select id, stream, topic
            from projects;
        """)
        return [Project(
            elem["id"],
            elem["stream"],
            elem["topic"]
        ) for elem in res]

    async def delete(self, project_id: int) -> None:
        await self.pool.execute("""
            delete
            from projects
            where id = $1
        """, project_id)
