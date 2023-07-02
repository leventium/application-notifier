import asyncpg


class Database:
    async def __init_database(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id          INT PRIMARY KEY,
                stream      VARCHAR(150),
                topic       VARCHAR(150)
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

    async def get_subscribed_projects(self) -> list:
        res = await self.conn.fetch("""
            SELECT id, stream, topic
            FROM projects;
        """)
        return [dict(elem) for elem in res]

    async def get_project_applications(self, project_id: int):
        res = await self.conn.fetch("""
            SELECT id, name, role, project_id
            FROM applications
            WHERE project_id = $1;
        """, project_id)
        return [dict(elem) for elem in res]

    async def insert_project(
            self,
            project_id: int,
            stream: str,
            topic: str) -> None:
        try:
            await self.conn.execute("""
                INSERT INTO projects (id, stream, topic)
                    VALUES ($1, $2, $3);
            """, project_id, stream, topic)
        except asyncpg.UniqueViolationError:
            raise ProjectAlreadyExistsError()

    async def insert_application(
            self,
            app_id: int,
            project_id: int,
            user_name: str,
            role: str):
        try:
            await self.conn.execute(
                """
                INSERT INTO applications (id, name, role, project_id)
                    VALUES ($1, $2, $3, $4);
                """, app_id, user_name, role, project_id)
        except KeyError as err:
            raise InvalidApplication(err.args[0])
        except asyncpg.UniqueViolationError:
            raise ApplicationAlreadyExistsError()

    async def project_exists(self, project_id: int) -> bool:
        return bool(await self.conn.fetchval("""
            SELECT COUNT(*)
            FROM projects
            WHERE id = $1
            LIMIT 1;
        """, project_id))

    async def delete_project(self, project_id: int) -> None:
        await self.conn.execute("""
            DELETE
            FROM projects
            WHERE id = $1;
        """, project_id)

    async def update_zulip_stream(
            self,
            project_id: int,
            stream: str,
            topic: str) -> None:
        await self.conn.execute("""
            UPDATE projects
            SET stream = $2, topic = $3
            WHERE id = $1;
        """, project_id, stream, topic)


class ProjectAlreadyExistsError(Exception):
    pass


class ApplicationAlreadyExistsError(Exception):
    pass


class InvalidApplication(Exception):
    pass
