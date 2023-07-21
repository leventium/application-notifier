from src.models.application import Application


class ApplicationService:
    @staticmethod
    def find_new_applications(
            new: list[Application],
            old: list[Application]) -> list[Application]:
        new_set = set(list(map(lambda x: x.id, new)))
        old_set = set(list(map(lambda x: x.id, old)))
        res_set = new_set - old_set
        res = []
        for app in new:
            if app.id in res_set:
                res.append(app)
        return res
