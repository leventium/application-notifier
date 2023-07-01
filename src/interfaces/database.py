import asyncpg


class Database:
    async def __init_database(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id          INT PRIMARY KEY,
                stream      VARCHAR(120),
                topic       VARCHAR(120)
            );
            
            CREATE TABLE IF NOT EXISTS applications (
                id          INT PRIMARY KEY,
                name        VARCHAR(120),
                role        VARCHAR(120),
                project_id  INT REFERENCES projects(id) ON DELETE CASCADE
            );
        """)

    @classmethod
    async def connect(
            cls,
            host: str,
            port: int,
            user: str,
            password: str,
            database: str):
        pool = asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        res = cls(pool)
        await res.__init_database()
        return res

    def __init__(self, conn):
        self.conn = conn

    async def close(self) -> None:
        await self.conn.close()

    # ---------------------------------------------------------------------

    async def insert_record(
            self,
            project_id: int,
            stream: str,
            topic: str,
            applications: list[dict]) -> None:
        async with self.conn.transaction():
            try:
                await self.conn.execute("""
                    INSERT INTO projects (id, stream, topic)
                        VALUES ($1, $2, $3);
                """, project_id, stream, topic)
            except asyncpg.UniqueViolationError:
                raise ProjectAlreadyExistsError(project_id)
            for app in applications:
                try:
                    await self.conn.execute(
                        """
                        INSERT INTO applications (id, name, role, project_id)
                            VALUES ($1, $2, $3, $4);
                        """,
                        app["id"],
                        app["name"],
                        app["role"],
                        app["project_id"]
                    )
                except KeyError as err:
                    raise InvalidApplication(err.args[0])
                except asyncpg.UniqueViolationError:
                    raise ProjectAlreadyExistsError(app["id"])

    async def update_zulip_channel(
            self,
            project_id: int,
            stream: str,
            topic: str) -> None:
        await self.conn.execute("""
            UPDATE projects
            SET stream = $2, topic = $3
            WHERE id = $1;
        """, project_id, stream, topic)

    async def exists(self, project_id: int) -> bool:
        return bool(await self.conn.fetchval("""
            SELECT COUNT(*)
            FROM projects
            WHERE id = $1
            LIMIT 1;
        """, project_id))

    async def delete_record(self, project_id: int) -> None:
        await self.conn.execute("""
            DELETE
            FROM projects
            WHERE id = $1;
        """, project_id)

    async def insert_application(self, applications: list):
        async with self.conn.transaction():
            for app in applications:
                try:
                    await self.conn.execute(
                        """
                        INSERT INTO applications (id, name, role, project_id)
                            VALUES ($1, $2, $3, $4);
                        """,
                        app["id"],
                        app["name"],
                        app["role"],
                        app["project_id"]
                    )
                except KeyError as err:
                    raise InvalidApplication(err.args[0])
                except asyncpg.UniqueViolationError:
                    raise ApplicationAlreadyExistsError(app["id"])

    async def get_all_applications(self, project_id: int):
        res = await self.conn.fetch("""
            SELECT id, name, role, project_id
            FROM applications
            WHERE project_id = $1;
        """, project_id)
        return [dict(elem) for elem in res]

    async def get_subscribed_projects(self) -> list:
        res = await self.conn.fetch("""
            SELECT id, stream, topic
            FROM projects;
        """)
        return [dict(elem) for elem in res]


class ProjectAlreadyExistsError(Exception):
    pass


class ApplicationAlreadyExistsError(Exception):
    pass


class InvalidApplication(Exception):
    pass
