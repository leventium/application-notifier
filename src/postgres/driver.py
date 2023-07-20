import asyncpg


class PostgresDriver(object):
    _instance = None

    def __new__(cls):
        return None

    @classmethod
    async def get_instance(
            cls,
            host: str,
            port: int,
            user: str,
            password: str,
            db: str):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance.pool = asyncpg.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db
            )
            async with cls._instance.pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id          INT PRIMARY KEY,
                        stream      VARCHAR(150),
                        topic       VARCHAR(150)
                    );
                    
                    CREATE TABLE IF NOT EXISTS applications (
                        id          INT PRIMARY KEY,
                        name        VARCHAR(120),
                        role        VARCHAR(120),
                        project_id  INT REFERENCES projects(id)
                                    ON DELETE CASCADE
                    );
                """)
        return cls._instance

    async def get_connection(self):
        return await self._instance.pool.acquire()

    async def release_conection(self, conn):
        await self._instance.pool.release(conn)
