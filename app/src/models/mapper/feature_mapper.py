import json
import pandas as pd
from src.models.entity.feature import Feature
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class FeatureMapper(DataMapper):
    @staticmethod
    def get_list_of_feature_options():
        data_path = Constants.FilePaths.FEATURES_DATA_JSON_PATH
        data_handler = DataMapper(data_path).get_composed_data_frame()

        list_of_features = []
        for key, value in data_handler.items():
            feature = Feature.from_dict(value)
            list_of_features.append(str(feature))

        return list_of_features

    @staticmethod
    def get_features_as_entities():
        data_path = Constants.FilePaths.FEATURES_DATA_JSON_PATH
        data_handler = DataMapper(data_path).get_composed_data_frame()

        return [Feature.from_dict(value) for value in data_handler.values()]