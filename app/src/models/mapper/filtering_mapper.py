import json
import pandas as pd
import src.controllers.app_path_config as app_path_config
from src.models.entity.test_category import TestCategory
from src.models.mapper.data_mapper import DataMapper
from collections import defaultdict


class FilteringMapper(DataMapper):

    @staticmethod
    def filter_test_names_and_times_dictionary(
        data_path=app_path_config.get_data_storage_path(),
    ):
        test_names = []
        total_times = []
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            test_name = value.get("test_name")
            total_time = value.get("total_time")

            if test_name is not None and total_time is not None:
                test_names.append(test_name)
                total_times.append(total_time)

        return {"test_name": test_names, "total_time": total_times}

    def filter_test_category_and_approaches(
        data_path=app_path_config.get_data_storage_path(),
    ):
        data = []
        category_approach_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

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
        filter_by_key="",
        filter_by_value="",
    ):
        data = []
        category_approach_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

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

        data.sort(key=lambda prop: prop["level"])
        return data

    def filter_test_suites(
        data_path=app_path_config.get_data_storage_path(),
    ):
        data = []
        suite_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            test_suite = value.get("test_suite")
            total_time = value.get("total_time")

            suite_counts[(test_suite)] += 1

        print("Test Counts per Suite:", dict(suite_counts))

        data = [
            {
                "test_suites": suite,
                "total_time": total_time,
                "count": count,
            }
            for (suite), count in suite_counts.items()
        ]

        return data
