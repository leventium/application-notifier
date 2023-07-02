"""
Module that contains definition for application class.
"""
from src.interfaces.database import Database


class Application:
    """
    A class that represents applications of project.
    """
    def __init__(
            self,
            app_id: int,
            project_id: int,
            user_name: str,
            role: str):
        """
        Creates the instance of applications class.
        """
        self.id = app_id
        self.project_id = project_id
        self.user_name = user_name
        self.role = role

    async def insert_into_database(self, db: Database):
        """
        Inserts this applications in the database.
        """
        await db.insert_application(
            self.id,
            self.project_id,
            self.user_name,
            self.role
        )
