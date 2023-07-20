"""
Module that contains definition for project class.
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
