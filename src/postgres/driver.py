import os
import asyncpg


class PostgresDriver(object):
    _instance = None
    _pool = None

    def __new__(cls):
        return None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._pool = asyncpg.create_pool(
                host=os.environ["PG_HOST"],
                port=int(os.environ["PG_PORT"]),
                user=os.environ["PG_USER"],
                password=os.environ["PG_PASSWORD"],
                database=os.environ["PG_DATABASE"]
            )
            async with cls._instance._pool.acquire() as conn:
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
        return await self._pool.acquire()

    async def release_connection(self, conn):
        await self._pool.release(conn)
