"""
Module that contains definition for models classes.
"""


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
