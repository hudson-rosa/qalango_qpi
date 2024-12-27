import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.suite_mapper import SuiteMapper
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_feature_or_tests as html_register_feature_or_tests
from src.utils.data_generator import DataGenerator
from src.utils.file_handler import FileHandler
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils


app = dash.Dash(__name__)
ctx = dash.callback_context

features_json_storage = Constants.FilePaths.FEATURES_DATA_JSON_PATH
features_mapper_instance = DataMapper(filename=features_json_storage)

scripted_tests_json_storage = Constants.FilePaths.SCRIPTED_TESTS_DATA_JSON_PATH
test_cases_mapper_instance = DataMapper(filename=scripted_tests_json_storage)


@callback(
    Output("rf--feature-or-test-id", "value"),
    [
        Input("rf--bdd-container", "style"),
        Input("rf--scripted-container", "style"),
        Input("rf--generate-id-button", "n_clicks"),
    ],
    prevent_initial_call=False,
)
def update_random_id(bdd_style, scripted_style, n_clicks):
    if bdd_style.get("display") == "block":
        prefix = "idfeat_"
    elif scripted_style.get("display") == "block":
        prefix = "idtest_"
    else:
        prefix = "unknown_"

    return prefix + DataGenerator.generate_aggregated_uuid()


@callback(
    Output("rf--suite-dropdown", "options"), [Input("rf--project-dropdown", "value")]
)
def update_suite_options(selected_project):
    if not selected_project:
        return []
    project_id = str(selected_project).split("(")[1].rstrip(")")
    return SuiteMapper.get_suite_options(project_id=project_id)


@callback(
    [
        Output("rf--bdd-container", "style"),
        Output("rf--scripted-container", "style"),
        Output("rf--toggle-bdd", "className"),
        Output("rf--toggle-scripted", "className"),
    ],
    [Input("rf--toggle-bdd", "n_clicks"), Input("rf--toggle-scripted", "n_clicks")],
)
def toggle_form(bdd_clicks, scripted_clicks):
    bdd_toggle_style = {"display": "block"}
    scripted_toggle_style = {"display": "none"}
    bdd_class = "toggle-btn active"
    scripted_class = "toggle-btn"

    if ctx.triggered_id == "rf--toggle-scripted":
        bdd_toggle_style = {"display": "none"}
        scripted_toggle_style = {"display": "block"}
        bdd_class = "toggle-btn"
        scripted_class = "toggle-btn active"

    return bdd_toggle_style, scripted_toggle_style, bdd_class, scripted_class


@callback(
    Output("rf--preconditions-container", "children"),
    Input("rf--add-precondition", "n_clicks"),
    State("rf--preconditions-container", "children"),
)
def add_test_precondition(n_clicks, existing_preconditions):
    if n_clicks > 0:
        precond_block_number = (len(existing_preconditions)) + 1

        new_precondition = dcc.Textarea(
            id=f"rf--precondition-{precond_block_number}",
            placeholder=f"Enter precondition {precond_block_number}",
        )
        return existing_preconditions + [new_precondition]

    return existing_preconditions


@callback(
    Output("rf--steps-container", "children"),
    Input("rf--add-step", "n_clicks"),
    State("rf--steps-container", "children"),
)
def add_test_step(n_clicks, existing_steps):
    if n_clicks > 0:
        step_block_number = (len(existing_steps) // 2) + 1

        new_step = dcc.Textarea(
            id=f"rf--step-{step_block_number}",
            placeholder=f"Enter step {step_block_number}",
        )
        new_expected = dcc.Textarea(
            id=f"rf--expected-{step_block_number}",
            placeholder=f"Enter expected result {step_block_number}",
        )
        return existing_steps + [new_step, new_expected]

    return existing_steps


@callback(
    Output("rf--bdd-editor", "style"),
    Input("rf--bdd-editor", "value"),
    State("rf--bdd-editor", "style"),
)
def auto_resize_textarea(content, current_style):
    if content:
        line_count = str(content).count("\n") + 1
        new_dynamic_height = min(100 + line_count * 20, 800)
        updated_style = {**current_style, "height": f"{new_dynamic_height}px"}
        return updated_style
    return current_style


@callback(
    Output("rf--bdd-output-message", "children"),
    [
        Input("rf--submit-bdd-button", "n_clicks"),
        Input("rf--delete-bdd-file-button", "n_clicks"),
    ],
    [
        State("rf--feature-or-test-id", "value"),
        State("rf--feature-name", "value"),
        State("rf--bdd-editor", "value"),
        State("rf--suite-dropdown", "value"),
        State("rf--project-dropdown", "value"),
    ],
)
def submit_bdd_data(
    submit_clicks,
    delete_file_clicks,
    feature_id="",
    feature_name="",
    bdd_content="",
    suite_ref="",
    project_ref="",
):
    ctx = dash.callback_context
    feature_name_underlined = str(feature_name).strip().replace(" ", "_")
    feature_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{feature_id}--{feature_name_underlined.lower()}.feature"

    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rf--submit-bdd-button":
            is_valid, message = ValidationUtils.validate_mandatory_fields(
                feature_id=feature_id,
                feature_name=feature_name,
                bdd_content=bdd_content,
                suite_ref=suite_ref,
                project_ref=project_ref,
            )
            if not is_valid:
                return message, None

            try:
                data = features_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            bdd_content_lower = str(bdd_content).lower()
            project_id = str(project_ref).split("(")[1].rstrip(")")
            project_name = str(project_ref).split("(")[0].strip()
            suite_name = str(suite_ref).split("(")[0].strip()

            scenarios_count = bdd_content_lower.count(
                "scenario:"
            ) + bdd_content_lower.count("scenario outline:")

            new_data = {
                Constants.FeaturesDataJSON.FEATURE_ID: feature_id,
                Constants.FeaturesDataJSON.FEATURE_NAME: feature_name_underlined,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: scenarios_count,
                "test_levels": {
                    Constants.FeaturesDataJSON.QTY_OF_INTEGRATION: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.INTEGRATION}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_COMPONENT: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.COMPONENT}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_CONTRACT: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.CONTRACT}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_API: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.API}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_E2E: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.E2E}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.PERFORMANCE}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_SECURITY: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.SECURITY}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_USABILITY: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.USABILITY}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY: bdd_content_lower.count(
                        f"@{Constants.TestLevelsEntity.EXPLORATORY}"
                    ),
                },
                "test_approaches": {
                    Constants.FeaturesDataJSON.QTY_OF_AUTOMATED: bdd_content_lower.count(
                        f"@{Constants.TestTypesEntity.AUTOMATED}"
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_MANUAL: scenarios_count
                    - bdd_content_lower.count(
                        f"@{Constants.TestTypesEntity.AUTOMATED}"
                    ),
                },
            }

            if project_id not in data:
                data[project_id] = {
                    Constants.ProjectDataJSON.PROJECT_NAME: project_name,
                    Constants.SuiteDataJSON.SUITE_REF: suite_ref,
                    "scenarios": [],
                }

            data[project_id]["scenarios"].append(new_data)

            features_mapper_instance.save_to_json_storage(data)

            features_mapper_instance.save_content_to_new_file(
                new_file=feature_file_pathname, new_data=bdd_content
            )

            return (
                html.Pre(f"BDD Feature saved successfully:\n\n{feature_file_pathname}"),
                DataGenerator.generate_aggregated_uuid(),
            )

        case "rf--delete-bdd-file-button":
            try:
                data = features_mapper_instance.load_from_json_storage()

                FileHandler.delete_file(feature_file_pathname)

                if feature_id in data:
                    del data[feature_id]

                    features_mapper_instance.save_to_json_storage(data)

                    return (
                        None,
                        f"Feature file deleted successfully",
                    )
                else:
                    return (
                        None,
                        f"Feature file was not found",
                    )
            except FileNotFoundError:
                return None, "Deletion not possible. The JSON file was not found."

        case _:
            return "Please fill out the fields before submitting a feature file", None


@callback(
    Output("rf--scripted-output-message", "children"),
    Input("rf--submit-scripted-button", "n_clicks"),
    [
        State("rf--feature-or-test-id", "value"),
        State("rf--test-name", "value"),
        State("rf--preconditions-container", "children"),
        State("rf--steps-container", "children"),
        State("rf--test-level", "value"),
        State("rf--test-approach", "value"),
        State("rf--suite-dropdown", "value"),
        State("rf--project-dropdown", "value"),
    ],
)
def submit_scripted_test(
    submit_clicks,
    test_id="",
    test_name="",
    preconditions_children="",
    steps_children="",
    test_level="",
    test_approach="",
    suite_ref="",
    project_ref="",
):
    ctx = dash.callback_context
 
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rf--submit-scripted-button":
            is_valid, message = ValidationUtils.validate_mandatory_fields(
                feature_id=test_id,
                test_name=test_name,
                preconditions_children=preconditions_children,
                steps_children=steps_children,
                test_level=test_level,
                suite_ref=suite_ref,
                project_ref=project_ref,
            )
            if not is_valid:
                return message, None

            try:
                data = features_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            preconditions_data = []
            for i in range(0, len(preconditions_children), 2):
                precond_textarea = preconditions_children[i]
                step_value = precond_textarea.get("props", {}).get("value", "").strip()

                preconditions_data.append({"precondition": step_value})

            steps_and_expected_data = []
            for i in range(0, len(steps_children), 2):
                step_textarea = steps_children[i]
                expected_textarea = steps_children[i + 1]

                step_value = step_textarea.get("props", {}).get("value", "").strip()
                expected_value = (
                    expected_textarea.get("props", {}).get("value", "").strip()
                )

                steps_and_expected_data.append(
                    {"step": step_value, "expected": expected_value}
                )

            if (
                not test_id
                or not test_name
                or any(not s["step"] for s in steps_and_expected_data)
            ):
                return "All fields (Feature ID, Test Title, and Steps) must be filled."

            project_id = str(project_ref).split("(")[1].rstrip(")")
            project_name = str(project_ref).split("(")[0].strip()
            suite_name = str(suite_ref).split("(")[0].strip()

            new_data = {
                Constants.TestEffortsDataJSON.TEST_ID: test_id,
                Constants.TestEffortsDataJSON.TEST_NAME: test_name,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: 1,
                "test_script": {
                    "preconditions": preconditions_data,
                    "steps": steps_and_expected_data,
                },
                "test_levels": {
                    Constants.FeaturesDataJSON.QTY_OF_INTEGRATION: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.INTEGRATION
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_COMPONENT: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.COMPONENT
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_CONTRACT: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.CONTRACT
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_API: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.API
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_E2E: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.E2E
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.PERFORMANCE
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_SECURITY: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.SECURITY
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_USABILITY: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.USABILITY
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY: is_matching_test_level(
                        test_level, Constants.TestLevelsEntity.EXPLORATORY
                    ),
                },
                "test_approaches": {
                    Constants.FeaturesDataJSON.QTY_OF_AUTOMATED: is_matching_test_level(
                        test_approach, Constants.TestTypesEntity.AUTOMATED
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_MANUAL: is_matching_test_level(
                        test_approach, Constants.TestTypesEntity.MANUAL
                    ),
                },
            }

            if project_id not in data:
                data[project_id] = {
                    Constants.ProjectDataJSON.PROJECT_NAME: project_name,
                    Constants.SuiteDataJSON.SUITE_REF: suite_ref,
                    "scenarios": [],
                }

            data[project_id]["scenarios"].append(new_data)

            test_cases_mapper_instance.save_to_json_storage(data)

            return (
                html.Pre(f"Test Case saved successfully"),
                None,
            )
        case _:
            return "Please fill out the fields before submitting a test case", None


def is_matching_test_level(current_test_level, expected=""):
    return int(current_test_level == expected)


app.layout = html_register_feature_or_tests.render_layout()
