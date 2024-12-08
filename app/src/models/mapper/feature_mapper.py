import json
import pandas as pd
import src.controllers.app_path_config as app_path_config
from src.models.mapper.data_mapper import DataMapper


class ProjectMapper(DataMapper):

    @staticmethod
    def get_feature_options():
        data_path = app_path_config.get_data_storage_features_path()
        data_handler = DataMapper(data_path).get_composed_data_frame()
        
        list_of_features = []
        for key, value in data_handler.items():
            feature_title = value.get("feature_title")
            feature_id = value.get("feature_id")
            list_of_features.append(f"{feature_title} ({feature_id})")

        return list_of_features
