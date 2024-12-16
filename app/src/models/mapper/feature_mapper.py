import json
import pandas as pd
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants


class FeatureMapper(DataMapper):

    @staticmethod
    def get_list_of_feature_options():
        data_path = Constants.FilePaths.FEATURES_DATA_JSON_PATH
        data_handler = DataMapper(data_path).get_composed_data_frame()

        list_of_features = []
        for key, value in data_handler.items():
            feature_name = value.get(Constants.FeaturesDataJSON.FEATURE_NAME)
            feature_id = value.get(Constants.FeaturesDataJSON.FEATURE_ID)
            list_of_features.append(f"{feature_name} ({feature_id})")

        return list_of_features
