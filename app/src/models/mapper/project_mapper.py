import json
import pandas as pd
from src.models.entity.project import Project
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class ProjectMapper(DataMapper):

    @staticmethod
    def get_project_options():
        project_data_path = Constants.FilePaths.PROJECTS_DATA_JSON_PATH
        data_handler = DataMapper(project_data_path).get_composed_data_frame()

        list_of_projects = []
        for key, value in data_handler.items():
            project = Project.from_dict(value)
            list_of_projects.append(str(project))

        return list_of_projects

    @staticmethod
    def get_projects_as_entities():
        project_data_path = Constants.FilePaths.PROJECTS_DATA_JSON_PATH
        data_handler = DataMapper(project_data_path).get_composed_data_frame()

        return [Project.from_dict(value) for value in data_handler.values()]
