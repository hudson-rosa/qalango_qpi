import json
import pandas as pd
from src.models.entity.test_categories import TestCategory
from src.models.entity.test_level import TestLevel
from src.models.mapper.data_mapper import DataMapper
from src.utils.constants.constants import Constants
from collections import defaultdict

from src.utils.string_handler import StringHandler


class EditScenariosMapper(DataMapper):

    def get_data():
        return DataMapper(
            Constants.FilePaths.SCENARIOS_DATA_JSON_PATH
        ).load_from_json_storage()

    def get_project_items():
        return {
            proj_id: details["project_id"]
            for proj_id, details in EditScenariosMapper.get_data().items()
        }

    def parse_scenarios_data(project_id):
        data = EditScenariosMapper.get_data()
        rows = []

        for proj_id, proj_data in data.items():
            if project_id and proj_id != project_id:
                continue
            for suite_id, suite_data in proj_data.items():
                if not str(suite_id).startswith("idsuite_"):
                    continue
                for feature in suite_data["feature_specs"]:
                    for scenario in feature["scenarios"]:
                        rows.append(
                            {
                                "Suite ID": suite_id,
                                "Suite": suite_data["suite_name"],
                                "Feature ID": feature["spec_doc_id"],
                                "Feature Name": feature.get(
                                    "feature_name", feature.get("test_name", "")
                                ),
                                "Requirements Link": scenario.get(
                                    "requirements_link"
                                ),
                                "Scenario ID": scenario["scenario_id"],
                                "Scenario Name": scenario["scenario_name"],
                                "Test Level": scenario["test_level"],
                                "Test Approach": scenario["test_approach"],
                                "Test Categories": ", ".join(
                                    scenario["test_categories"]
                                ),
                                "Test Duration": scenario["test_duration"],
                                "Content": scenario["content"],
                            }
                        )
        return rows
