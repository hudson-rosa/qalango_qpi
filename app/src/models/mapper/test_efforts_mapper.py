import json
import pandas as pd
from src.models.entity.test_categories import TestCategory
from src.models.entity.test_level import TestLevel
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants
from collections import defaultdict

from src.utils.string_handler import StringHandler


class TestEffortsMapper(DataMapper):

    @staticmethod
    def get_project_data(project_id, data_handler):
        """
        Retrieves all feature specifications for a given project ID.
        """
        project_data = data_handler.get(StringHandler.get_id_format(project_id))

        # Handle the case where project_data is a Pandas Series
        if isinstance(project_data, pd.Series):
            project_data = project_data.dropna().to_dict()

        # Check if project_data is None, empty, or invalid
        if not project_data or not isinstance(project_data, dict):
            print(f"No data found for project ID {project_id}")
            return [], []

        # Extract `feature_specs` from all suites
        feature_specs = []
        scenario = []
        for suite_id, suite_data in project_data.items():
            if suite_id == "project_name":
                continue  # Skip the project_name field

            suite_feature_specs = suite_data.get("feature_specs", [])
            if isinstance(suite_feature_specs, list):
                feature_specs.extend(suite_feature_specs)
            elif isinstance(suite_feature_specs, dict):
                # Handle edge cases where feature_specs might be a dict
                feature_specs.append(suite_feature_specs)

            for scenario_data in suite_feature_specs:
                scenarios_specs = scenario_data.get("scenarios", [])
                scenario.append(scenarios_specs)

        return feature_specs or [], scenario or []

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

    @staticmethod
    def sum_test_approaches_by_project(
        project_id, data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH
    ):
        """
        Sum the quantities of automated and manual tests for a specific project.
        """
        # Load JSON data
        data_handler = DataMapper(data_path).get_composed_data_frame()
        feature_specs = TestEffortsMapper.get_project_data(project_id, data_handler)[0]

        if not feature_specs:
            print(f"No feature specifications found for project ID {project_id}")
            return []

        # Initialize counters
        total_automated = 0
        total_manual = 0

        # Iterate through feature_specs to sum test approaches
        for feature in feature_specs:
            test_approaches = feature.get(
                Constants.FeaturesDataJSON.TEST_APPROACHES, {}
            )
            if not isinstance(test_approaches, dict):
                print(f"Invalid 'test_approaches' format: {test_approaches}")
                continue

            # Dynamically extract and sum automated and manual tests
            qty_automated = test_approaches.get(
                Constants.FeaturesDataJSON.QTY_OF_AUTOMATED, 0
            )
            qty_manual = test_approaches.get(
                Constants.FeaturesDataJSON.QTY_OF_MANUAL, 0
            )

            # Ensure proper data type
            total_automated += (
                int(qty_automated) if isinstance(qty_automated, (int, float)) else 0
            )
            total_manual += (
                int(qty_manual) if isinstance(qty_manual, (int, float)) else 0
            )

        # Prepare data for the pie chart
        data = [
            {
                Constants.ScenariosDataJSON.TEST_APPROACH: Constants.TestTypesEntity.AUTOMATED,
                Constants.ScenariosDataJSON.COUNT: total_automated,
            },
            {
                Constants.ScenariosDataJSON.TEST_APPROACH: Constants.TestTypesEntity.MANUAL,
                Constants.ScenariosDataJSON.COUNT: total_manual,
            },
        ]

        return data

    @staticmethod
    def filter_test_suites_by_project(
        project_id, data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH
    ):
        """
        Count the quantity of scenarios per suite for a specific project.
        """
        data_handler = DataMapper(data_path).get_composed_data_frame()
        project_data = TestEffortsMapper.get_project_data(project_id, data_handler)[0]

        if not project_data:
            return []

        # Prepare the result list
        suite_scenario_counts = []

        # Iterate over each suite in the project
        for suite_id, suite_data in data_handler.get(
            StringHandler.get_id_format(project_id)
        ).items():
            if not isinstance(suite_data, dict):
                continue

            if suite_id == "project_name":
                continue

            suite_name = suite_data.get("suite_name", "Unknown Suite")
            feature_specs = suite_data.get("feature_specs", [])

            # Sum qty_of_scenarios for all features in this suite
            total_scenarios = 0
            if isinstance(feature_specs, list):
                total_scenarios = sum(
                    spec.get("qty_of_scenarios", 0)
                    for spec in feature_specs
                    if isinstance(spec, dict)
                )
            elif isinstance(feature_specs, dict):
                total_scenarios = feature_specs.get("qty_of_scenarios", 0)

            # Add the suite data to the result list
            suite_scenario_counts.append(
                {
                    Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                    Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: total_scenarios,
                }
            )

        return suite_scenario_counts

    @staticmethod
    def filter_test_level_and_approaches_by_project(
        project_id,
        data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH,
        filter_by_key="",
        filter_by_value="",
    ):
        data = []
        level_approach_counts = defaultdict(int)
        data_handler = DataMapper(data_path).get_composed_data_frame()
        feature_specs = TestEffortsMapper.get_project_data(project_id, data_handler)[1]

        if not feature_specs:
            print(f"No feature specifications found for project ID {project_id}")
            return []

        for item in feature_specs:
            # Handle nested lists
            if isinstance(item, list):
                for feature in item:
                    test_level = feature.get(Constants.ScenariosDataJSON.TEST_LEVEL)
                    test_approach = feature.get(
                        Constants.ScenariosDataJSON.TEST_APPROACH
                    )

                    # Filter and count
                    if feature.get(filter_by_key) == filter_by_value:
                        level_approach_counts[(test_level, test_approach)] += 1

            # Handle dictionaries directly
            elif isinstance(item, dict):
                test_level = item.get(Constants.ScenariosDataJSON.TEST_LEVEL)
                test_approach = item.get(Constants.ScenariosDataJSON.TEST_APPROACH)

                # Filter and count
                if item.get(filter_by_key) == filter_by_value:
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

    @staticmethod
    def filter_counted_test_level_and_approaches_by_project(
        project_id, data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH
    ):
        data_handler = DataMapper(data_path).get_composed_data_frame()
        feature_specs = TestEffortsMapper.get_project_data(project_id, data_handler)[0]

        if not feature_specs:
            print(f"No feature specifications found for project ID {project_id}")
            return []

        # Initialize counters for test levels and approaches
        totals = defaultdict(int)
        test_approach_keys = [
            Constants.FeaturesDataJSON.QTY_OF_AUTOMATED,
            Constants.FeaturesDataJSON.QTY_OF_MANUAL,
        ]
        test_level_keys = [
            Constants.FeaturesDataJSON.QTY_OF_INTEGRATION,
            Constants.FeaturesDataJSON.QTY_OF_COMPONENT,
            Constants.FeaturesDataJSON.QTY_OF_CONTRACT,
            Constants.FeaturesDataJSON.QTY_OF_API,
            Constants.FeaturesDataJSON.QTY_OF_E2E,
            Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE,
            Constants.FeaturesDataJSON.QTY_OF_SECURITY,
            Constants.FeaturesDataJSON.QTY_OF_USABILITY,
            Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY,
        ]

        # Iterate through feature_specs to sum test approaches and levels
        for feature in feature_specs:
            test_approaches = feature.get(
                Constants.FeaturesDataJSON.TEST_APPROACHES, {}
            )
            test_levels = feature.get(Constants.FeaturesDataJSON.TEST_LEVELS, {})

            if not isinstance(test_levels, dict) or not isinstance(
                test_approaches, dict
            ):
                print(f"Invalid data format in feature: {feature}")
                continue

            # Sum quantities dynamically
            for key in test_approach_keys + test_level_keys:
                totals[key] += int(
                    test_approaches.get(key, 0)
                    if key in test_approaches
                    else test_levels.get(key, 0)
                )

        # Prepare data for the pie chart
        counted_levels = {
            Constants.TestLevelsEntity.INTEGRATION: totals[
                Constants.FeaturesDataJSON.QTY_OF_INTEGRATION
            ],
            Constants.TestLevelsEntity.COMPONENT: totals[
                Constants.FeaturesDataJSON.QTY_OF_COMPONENT
            ],
            Constants.TestLevelsEntity.CONTRACT: totals[
                Constants.FeaturesDataJSON.QTY_OF_CONTRACT
            ],
            Constants.TestLevelsEntity.API: totals[
                Constants.FeaturesDataJSON.QTY_OF_API
            ],
            Constants.TestLevelsEntity.E2E: totals[
                Constants.FeaturesDataJSON.QTY_OF_E2E
            ],
            Constants.TestLevelsEntity.PERFORMANCE: totals[
                Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE
            ],
            Constants.TestLevelsEntity.SECURITY: totals[
                Constants.FeaturesDataJSON.QTY_OF_SECURITY
            ],
            Constants.TestLevelsEntity.USABILITY: totals[
                Constants.FeaturesDataJSON.QTY_OF_USABILITY
            ],
            Constants.TestLevelsEntity.EXPLORATORY: totals[
                Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY
            ],
        }

        data = [
            {
                Constants.ScenariosDataJSON.TEST_LEVEL: level,
                "count": count,
                "level": TestLevel().get_option(
                    property_to_pick="tier", from_level=level
                ),
            }
            for level, count in counted_levels.items()
        ]

        data.sort(key=lambda prop: prop["level"])
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
