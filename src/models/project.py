"""
Module that contains definition for project class.
"""
from src.interfaces.database import Database
from application import Application


class Project:
    """
    A class that represents the MIEM project.
    """
    def __init__(self, project_id: int, zulip_channel: str, zulip_topic: str):
        """
        Creates the instance of project class.
        """
        self.id = project_id
        self.zulip_channel = zulip_channel
        self.zulip_topic = zulip_topic

    async def exists_in_database(self, db: Database) -> bool:
        """
        Check that this project exists in specified database.
        """
        pass

    async def insert_into_database(self, db: Database):
        """
        Insert this project into specified database.
        """
        pass

    async def get_applications_from_database(
            self, db: Database) -> list[Application]:
        """
        Get all applications of this project.
        """
        pass

    async def update_zulip_info(
            self, db: Database, new_channel: str, new_topic: str):
        """
        Update zulip info for this project.
        """
        pass

    async def find_new_applications(
            self,
            db: Database,
            applications: list[Application]) -> list[Application]:
        """
        Receives a list of applications and looks
        for those that are not in the database.
        """
        pass

    @classmethod
    async def get_subscribed_projects(cls, db: Database) -> list:
        """
        Returns all projects that are in the database.
        """
        pass
