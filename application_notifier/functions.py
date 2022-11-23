import os
from dotenv import load_dotenv


def bring_to_mongo_format(applications: list(dict), project_id: int) -> list(dict):
    for elem in applications:
        elem["project_id"] = project_id
        elem["_id"] = elem["id"]
        del elem["id"]
    return applications


def get_env_variables() -> dict:
    load_dotenv()
    env = {}
    try:
        env["CABINET_URL"] = os.environ("CABINET_URL")
        env["MONGO"] = os.environ("MONGO_CONNSTRING")
        env["SECRET"] = f"Bearer {os.environ('SECRET')}"
    except KeyError:
        print(
            "CABINET_URL\nSECRET\n"
            "MONGO_CONNSTRING\n^^^^^\nMust be specified."
        )
        raise Exception()
    return env
