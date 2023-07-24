import os
import asyncpg


class PostgresDatabase(object):
    _pool = None

    def __new__(cls):
        return None

    @classmethod
    async def _init(cls):
        await cls._pool.execute("""
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

    @classmethod
    async def get_instance(
            cls,
            host: str,
            port: int,
            user: str,
            password: str,
            database: str
    ):
        if cls._pool is None:
            cls._pool = asyncpg.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            await cls._init()
        return cls._pool

    @classmethod
    async def close(cls):
        await cls._pool.close()
        cls._pool = None
