"""
Module that contains definition for project class.
"""
from src.interfaces.database import Database
from application import Application


class Project:
    """
    A class that represents the MIEM project.
    """
    def __init__(self, project_id: int, zulip_stream: str, zulip_topic: str):
        """
        Creates the instance of project class.
        """
        self.id = project_id
        self.zulip_stream = zulip_stream
        self.zulip_topic = zulip_topic

    async def exists_in_database(self, db: Database) -> bool:
        """
        Check that this project exists in specified database.
        """
        return await db.project_exists(self.id)

    async def insert_into_database(self, db: Database):
        """
        Insert this project into specified database.
        """
        await db.insert_project(
            self.id,
            self.zulip_stream,
            self.zulip_topic
        )

    async def get_applications_from_database(
            self, db: Database) -> list[Application]:
        """
        Get all applications of this project.
        """
        res = []
        for app in await db.get_project_applications(self.id):
            res.append(Application(
                app["id"],
                app["project_id"],
                app["name"],
                app["role"]
            ))
        return res

    async def update_zulip_info(
            self, db: Database, new_stream: str, new_topic: str):
        """
        Update zulip info for this project.
        """
        await db.update_zulip_stream(self.id, new_stream, new_topic)
        self.zulip_stream = new_stream
        self.zulip_topic = new_topic

    async def find_new_applications(
            self,
            db: Database,
            applications: list[Application]) -> list[Application]:
        """
        Receives a list of applications and looks
        for those that are not in the database.
        """
        curr_apps = await db.get_project_applications(self.id)
        new_apps_set = set(map(lambda x: x.id, applications))
        old_apps_set = set(map(lambda x: x.id, curr_apps))
        unique_apps = new_apps_set - old_apps_set
        res = []
        for app in applications:
            if app.id in unique_apps:
                res.append(app)
        return res

    @classmethod
    async def get_subscribed_projects(cls, db: Database) -> list:
        """
        Returns all projects that are in the database.
        """
        res = []
        for project in await db.get_subscribed_projects():
            res.append(cls(
                project["id"],
                project["stream"],
                project["topic"]
            ))
        return res
