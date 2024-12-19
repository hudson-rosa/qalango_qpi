import json
import pandas as pd
from src.models.entity.suite import Suite
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class SuiteMapper(DataMapper):

    @staticmethod
    def get_suite_options():
        suite_data_path = Constants.FilePaths.SUITES_DATA_JSON_PATH
        data_handler = DataMapper(suite_data_path).get_composed_data_frame()

        list_of_suites = []
        for key, value in data_handler.items():
            suite = Suite.from_dict(value)
            list_of_suites.append(str(suite))

        return list_of_suites

    @staticmethod
    def get_suites_as_entities():
        suite_data_path = Constants.FilePaths.SUITES_DATA_JSON_PATH
        data_handler = DataMapper(suite_data_path).get_composed_data_frame()

        return [Suite.from_dict(value) for value in data_handler.values()]
