"""
Module that contains definition for application class.
"""


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
