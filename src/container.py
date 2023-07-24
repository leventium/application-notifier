"""
Module providing DI container.
"""
import os
from src.postgres.database import PostgresDatabase
from src.postgres.project_repository import PostgresProjectRepository
from src.postgres.application_repository import PostgresApplicationRepository
from src.interfaces.cabinet_interface import CabinetInterface
from src.interfaces.zulip_interface import ZulipInterface
from src.checker.checker import Checker


class Container:
    @classmethod
    def get(cls, classname):
        if classname == PostgresDatabase:
            return PostgresDatabase.get_instance(
                host=os.environ["PG_HOST"],
                port=int(os.environ["PG_PORT"]),
                user=os.environ["PG_USER"],
                password=os.environ["PG_USER"],
                database=os.environ["PG_DATABASE"]
            )
        if classname == PostgresProjectRepository:
            return PostgresProjectRepository(cls.get(PostgresDatabase))
        if classname == PostgresApplicationRepository:
            return PostgresApplicationRepository(cls.get(PostgresDatabase))
        if classname == CabinetInterface:
            return CabinetInterface(os.environ["CABINET_URL"])
        if classname == ZulipInterface:
            return ZulipInterface(
                zulip_url=os.environ["ZULIP_URL"],
                bot_email=os.environ["BOT_EMAIL"],
                bot_token=os.environ["BOT_TOKEN"]
            )
        if classname == Checker:
            return Checker(
                cls.get(ZulipInterface),
                cls.get(CabinetInterface),
                cls.get(PostgresProjectRepository),
                cls.get(PostgresApplicationRepository)
            )
