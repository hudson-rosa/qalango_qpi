import json
import pandas as pd
import src.controllers.app_path_config as app_path_config
from src.models.mapper.data_mapper import DataMapper


class ProjectMapper(DataMapper):

    @staticmethod
    def get_project_options():
        data_path = app_path_config.get_data_storage_project_path()
        data_handler = DataMapper(data_path).get_composed_data_frame()
        
        list_of_projects = []
        for key, value in data_handler.items():
            project_name = value.get("project_name")
            project_id = value.get("project_id")
            list_of_projects.append(f"{project_name} ({project_id})")

        return list_of_projects
