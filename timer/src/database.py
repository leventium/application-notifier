import os
import pymongo


class Database:
    def __init__(self, connstring: str):
        self.mongo = pymongo.MongoClient(os.environ["MONGO_CONNSTRING"])

    def insert_record(
            self, project_id: int,
            stream: str,
            topic: str,
            applications: list[dict]) -> None:
        for elem in applications:
            elem["project_id"] = project_id
            elem["_id"] = elem["id"]
            del elem["id"]
        self.mongo.db.subscribed_projects.insert_one({
            "_id": project_id,
            "stream": stream,
            "topic": topic
        })
        self.mongo.db.applications.insert_many(applications)

    def update_zulip_channel(
            self, project_id: int,
            stream: str,
            topic: str) -> None:
        self.mongo.db.subscribed_projects.update_one(
            {"_id": project_id},
            {"$set": {
                "stream": stream,
                "topic": topic
            }}
        )

    def exists(self, project_id: int) -> bool:
        return bool(tuple(
            self.mongo.db.subscribed_projects.find({"_id": project_id})
        ))

    def delete_record(self, project_id: int) -> None:
        self.mongo.db.applications.delete_many({"project_id": project_id})
        self.mongo.db.subscribed_projects.delete_one({"_id": project_id})

    def insert_application(self, applications: list):
        self.mongo.db.applications.insert_many(applications)

    def get_all_applications(self, project_id: int):
        return list(self.mongo.db.applications.find({"project_id": project_id}))

    def get_subscribed_projects(self) -> list:
        return list(self.mongo.db.subscribed_projects.find())

    def close(self) -> None:
        self.mongo.close()
