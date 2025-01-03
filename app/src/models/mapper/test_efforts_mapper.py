import json
import pandas as pd
from src.models.entity.test_categories import TestCategory
from src.models.entity.test_level import TestLevel
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants
from collections import defaultdict


class TestEffortsMapper(DataMapper):

    @staticmethod
    def filter_test_names_and_times_dictionary(
        data_path=Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH,
    ):
        test_names = []
        total_times = []
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            test_name = value.get(Constants.ScenariosDataJSON.TEST_NAME)
            total_time = value.get(Constants.ScenariosDataJSON.TOTAL_TIME)

            if test_name is not None and total_time is not None:
                test_names.append(test_name)
                total_times.append(total_time)

        return {
            Constants.ScenariosDataJSON.TEST_NAME: test_names,
            Constants.ScenariosDataJSON.TOTAL_TIME: total_times,
        }

    def filter_test_level_and_approaches(
        data_path=Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH,
    ):
        data = []
        level_approach_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            test_level = value.get(Constants.ScenariosDataJSON.TEST_LEVEL)
            test_approach = value.get(Constants.ScenariosDataJSON.TEST_APPROACH)

            level_approach_counts[(test_level, test_approach)] += 1

        print("Level and Approach Counts:", dict(level_approach_counts))

        data = [
            {
                Constants.ScenariosDataJSON.TEST_LEVEL: level,
                Constants.ScenariosDataJSON.TEST_APPROACH: approach,
                "count": count,
            }
            for (level, approach), count in level_approach_counts.items()
        ]

        return data

    def filter_test_level_and_approaches_by(
        data_path=Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH,
        filter_by_key="",
        filter_by_value="",
    ):
        data = []
        level_approach_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            test_level = value.get(Constants.ScenariosDataJSON.TEST_LEVEL)
            test_approach = value.get(Constants.ScenariosDataJSON.TEST_APPROACH)

            if value.get(filter_by_key) == filter_by_value:
                level_approach_counts[(test_level, test_approach)] += 1

        print("Level and Approach Counts:", dict(level_approach_counts))

        data = [
            {
                Constants.ScenariosDataJSON.TEST_LEVEL: level,
                Constants.ScenariosDataJSON.TEST_APPROACH: approach,
                "count": count,
                "level": TestLevel().get_option(
                    property_to_pick="tier", from_level=level
                ),
            }
            for (level, approach), count in level_approach_counts.items()
        ]

        data.sort(key=lambda prop: prop["level"])
        return data

    def filter_test_suites(
        data_path=Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH,
    ):
        data = []
        suite_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()

        for key, value in data_handler.items():
            suite_name = value.get(Constants.ScenariosDataJSON.SUITE_NAME)
            total_time = value.get(Constants.ScenariosDataJSON.TOTAL_TIME)

            suite_counts[(suite_name)] += 1

        print("Test Counts per Suite:", dict(suite_counts))

        data = [
            {
                Constants.ScenariosDataJSON.TOTAL_TIME: total_time,
                "number_of_test_suites": suite,
                "count": count,
            }
            for (suite), count in suite_counts.items()
        ]

        return data

    @staticmethod
    def get_list_of_test_levels():
        return [
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.UNIT
                ),
                "value": TestLevel().get_option("ref", Constants.TestLevelsEntity.UNIT),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.INTEGRATION
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.INTEGRATION
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.COMPONENT
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.COMPONENT
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.CONTRACT
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.CONTRACT
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.API
                ),
                "value": TestLevel().get_option("ref", Constants.TestLevelsEntity.API),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.E2E
                ),
                "value": TestLevel().get_option("ref", Constants.TestLevelsEntity.E2E),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.PERFORMANCE
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.PERFORMANCE
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.SECURITY
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.SECURITY
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.USABILITY
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.USABILITY
                ),
            },
            {
                "label": TestLevel().get_option(
                    "label", Constants.TestLevelsEntity.EXPLORATORY
                ),
                "value": TestLevel().get_option(
                    "ref", Constants.TestLevelsEntity.EXPLORATORY
                ),
            },
        ]

    @staticmethod
    def get_list_of_test_categories():
        return [
            {
                "label": TestCategory().get_option(
                    "label", Constants.TestCategoriesEntity.CRITICAL_TEST
                ),
                "value": TestCategory().get_option(
                    "ref", Constants.TestCategoriesEntity.CRITICAL_TEST
                ),
            },
            {
                "label": TestCategory().get_option(
                    "label", Constants.TestCategoriesEntity.EDGE_CASE
                ),
                "value": TestCategory().get_option(
                    "ref", Constants.TestCategoriesEntity.EDGE_CASE
                ),
            },
            {
                "label": TestCategory().get_option(
                    "label", Constants.TestCategoriesEntity.SMOKE_TEST
                ),
                "value": TestCategory().get_option(
                    "ref", Constants.TestCategoriesEntity.SMOKE_TEST
                ),
            },
            {
                "label": TestCategory().get_option(
                    "label", Constants.TestCategoriesEntity.MOBILE
                ),
                "value": TestCategory().get_option(
                    "ref", Constants.TestCategoriesEntity.MOBILE
                ),
            },
            {
                "label": TestCategory().get_option(
                    "label", Constants.TestCategoriesEntity.DESKTOP
                ),
                "value": TestCategory().get_option(
                    "ref", Constants.TestCategoriesEntity.DESKTOP
                ),
            },
        ]
