from src.utils.constants.constants import Constants


class Project:
    def __init__(self, project_id: str, project_name: str):
        self.project_id = project_id
        self.project_name = project_name

    def __str__(self):
        return f"{self.project_name} ({self.project_id})"

    def to_dict(self):
        return {
            Constants.ProjectDataJSON.PROJECT_ID: self.project_id,
            Constants.ProjectDataJSON.PROJECT_NAME: self.project_name,
        }

    @staticmethod
    def from_dict(data: dict):
        return Project(
            project_id=data.get(Constants.ProjectDataJSON.PROJECT_ID),
            project_name=data.get(Constants.ProjectDataJSON.PROJECT_NAME),
        )
