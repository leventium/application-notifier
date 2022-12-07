import os


def bring_to_mongo_format(applications: list[dict],
                          project_id: int) -> list[dict]:
    for elem in applications:
        elem["project_id"] = project_id
        elem["_id"] = elem["id"]
        del elem["id"]
    return applications


def check_env(*args: str):
    for name in args:
        if os.getenv(name) is None:
            raise KeyError(
                f"No environment variable with name {name}. "
                f"{args} must be specified."
            )
