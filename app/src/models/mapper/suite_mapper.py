import json
import pandas as pd
from src.models.entity.suite import Suite
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class SuiteMapper(DataMapper):

    @staticmethod
    def get_suite_options(project_id=None):
        suite_data_path = Constants.FilePaths.SUITES_DATA_JSON_PATH
        data = DataMapper(suite_data_path).load_from_json_storage()

        list_of_suites = []
        if project_id and project_id in data:
            SuiteMapper.get_suite_based_on_provided_project(
                project_id, data, list_of_suites
            )
        else:
            SuiteMapper.get_all_suites_when_no_projects_is_provided(
                data, list_of_suites
            )

        return list_of_suites

    @staticmethod
    def get_suite_based_on_provided_project(project_id, data, list_of_suites):
        suites = data[project_id].get("suites", [])
        for suite in suites:
            data_ref = f'{suite["suite_name"]} ({suite["suite_id"]})'
            suite_option = {
                "label": data_ref,
                "value": data_ref,
            }
            list_of_suites.append(suite_option)
        return list_of_suites

    @staticmethod
    def get_all_suites_when_no_projects_is_provided(data, list_of_suites):
        for project in data.values():
            for suite in project.get("suites", []):
                data_ref = f'{suite["suite_name"]} ({suite["suite_id"]})'
                suite_option = {
                    "label": data_ref,
                    "value": data_ref,
                }
                return list_of_suites.append(suite_option)

    @staticmethod
    def get_suites_as_entities():
        suite_data_path = Constants.FilePaths.SUITES_DATA_JSON_PATH
        data_handler = DataMapper(suite_data_path).get_composed_data_frame()

        return [Suite.from_dict(value) for value in data_handler.values()]
