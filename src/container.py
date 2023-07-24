"""
Module providing DI container.
"""
import os
from src.postgres.database import PostgresDatabase
from src.postgres.project_repository import PostgresProjectRepository
from src.postgres.application_repository import PostgresApplicationRepository
from src.clients.cabinet_client import CabinetClient
from src.clients.zulip_client import ZulipClient
from src.checker.checker import Checker
from src.controllers import Controller


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
        if classname == CabinetClient:
            return CabinetClient(os.environ["CABINET_URL"])
        if classname == ZulipClient:
            return ZulipClient(
                zulip_url=os.environ["ZULIP_URL"],
                bot_email=os.environ["BOT_EMAIL"],
                bot_token=os.environ["BOT_TOKEN"]
            )
        if classname == Checker:
            return Checker(
                zulip=cls.get(ZulipClient),
                cabinet=cls.get(CabinetClient),
                project_repo=cls.get(PostgresProjectRepository),
                app_repo=cls.get(PostgresApplicationRepository)
            )
        if classname == Controller:
            return Controller(
                cabinet=cls.get(CabinetClient),
                project_repo=cls.get(PostgresProjectRepository),
                app_repo=cls.get(PostgresApplicationRepository)
            )
