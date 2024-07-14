import json
import pandas as pd
import src.controllers.app_path_config as app_path_config
from src.models.entity.test_category import TestCategory
from src.utils.json_data_handler import JsonDataHandler
from collections import defaultdict


class DataProcessing(JsonDataHandler):

    @staticmethod
    def filter_test_names_and_times_dictionary(
        data_path=app_path_config.get_data_storage_path(),
    ):
        test_names = []
        total_times = []
        data_handler = JsonDataHandler(data_path).compose_data_frame()

        for key, value in data_handler.items():
            test_name = value.get("test_name")
            total_time = value.get("total_time")

            if test_name is not None and total_time is not None:
                test_names.append(test_name)
                total_times.append(total_time)

        return {"test_name": test_names, "total_time": total_times}

    def filter_test_category_and_approaches(
        data_path=app_path_config.get_data_storage_path()
    ):
        data = []
        category_approach_counts = defaultdict(int)
        data_handler = JsonDataHandler(data_path).compose_data_frame()

        for key, value in data_handler.items():
            test_category = value.get("test_category") 
            test_approach = value.get("test_approach")

            category_approach_counts[(test_category, test_approach)] += 1

        print("Category and Approach Counts:", dict(category_approach_counts))

        data = [
            {
                "test_category": category,
                "test_approach": approach,
                "count": count,
            }
            for (category, approach), count in category_approach_counts.items()
        ]
        
        return data
    
    def filter_test_category_and_approaches_by(
        data_path=app_path_config.get_data_storage_path(),
        filter_by_key="", filter_by_value=""
    ):
        data = []
        category_approach_counts = defaultdict(int)
        data_handler = JsonDataHandler(data_path).compose_data_frame()

        for key, value in data_handler.items():
            test_category = value.get("test_category") 
            test_approach = value.get("test_approach")

            if value.get(filter_by_key) == filter_by_value:
                category_approach_counts[(test_category, test_approach)] += 1

        print("Category and Approach Counts:", dict(category_approach_counts))

        data = [
            {
                "test_category": category,
                "test_approach": approach,
                "count": count,
                "level": TestCategory().get_option(
                    property_to_pick="tier", from_category=category
                ),
            }
            for (category, approach), count in category_approach_counts.items()
        ]
        
        data.sort(key=lambda prop: prop['level'])
        return data
