import json
import pandas as pd
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class ProjectMapper(DataMapper):

    @staticmethod
    def get_project_options():
        project_data_path = Constants.FilePaths.PROJECTS_DATA_JSON_PATH
        data_handler = DataMapper(project_data_path).get_composed_data_frame()
        
        list_of_projects = []
        for key, value in data_handler.items():
            project_name = value.get(Constants.ProjectDataJSON.PROJECT_NAME)
            project_id = value.get(Constants.ProjectDataJSON.PROJECT_ID)
            list_of_projects.append(f"{project_name} ({project_id})")

        return list_of_projects
