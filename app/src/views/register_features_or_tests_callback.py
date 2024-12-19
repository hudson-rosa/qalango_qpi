import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_feature_or_tests as html_register_feature_or_tests
from src.utils.data_generator import DataGenerator
from src.utils.file_handler import FileHandler
from src.utils.constants.constants import Constants


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
        State("rf--project-name", "value"),
    ],
)
def submit_bdd_data(
    submit_clicks,
    delete_file_clicks,
    feature_id="",
    feature_name="",
    bdd_content="",
    project_name="",
):
    ctx = dash.callback_context
    feature_id_pattern = "idfeat_" + str(feature_id)
    feature_name_underlined = str(feature_name).strip().replace(" ", "_")
    feature_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{feature_id_pattern}--{feature_name_underlined.lower()}.feature"

    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rf--submit-bdd-button":
            try:
                data = features_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            bdd_content_lower = str(bdd_content).lower()
            new_data = {
                Constants.FeaturesDataJSON.FEATURE_ID: feature_id_pattern,
                Constants.FeaturesDataJSON.FEATURE_NAME: feature_name_underlined,
                Constants.ProjectDataJSON.PROJECT_NAME: str(project_name)
                .split("(")[1]
                .rstrip(")"),
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: bdd_content_lower.count(
                    "scenario:"
                )
                + bdd_content_lower.count("scenario outline:"),
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
                Constants.FeaturesDataJSON.QTY_OF_AUTOMATED: bdd_content_lower.count(
                    f"@{Constants.TestTypesEntity.AUTOMATED}"
                ),
            }
            data[feature_id_pattern] = new_data

            features_mapper_instance.save_to_json_storage(data)

            FileHandler.save_new_file(
                file_pathname=feature_file_pathname, content=bdd_content
            )

            return (
                html.Pre(f"BDD Feature saved successfully:\n\n{feature_file_pathname}"),
                None,
            )

        case "rf--delete-bdd-file-button":
            try:
                data = features_mapper_instance.load_from_json_storage()

                FileHandler.delete_file(feature_file_pathname)

                if feature_id_pattern in data:
                    del data[feature_id_pattern]

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
        State("rf--suite-name", "value"),
        State("rf--project-name", "value"),
    ],
)
def submit_scripted_test(
    submit_clicks,
    test_id="",
    test_name="",
    preconditions_children="",
    steps_children="",
    test_level="",
    suite_name="",
    project_name="",
):
    ctx = dash.callback_context
    test_id_pattern = "idtest_" + str(test_id)
    # test_name_underlined = str(test_name).strip().replace(" ", "_")
    # test_case_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{test_id_pattern}--{DataGenerator.truncate_longer_name(test_name_underlined).lower()}.testcase"

    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rf--submit-scripted-button":
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
                not test_id_pattern
                or not test_name
                or any(not s["step"] for s in steps_and_expected_data)
            ):
                return "All fields (Feature ID, Test Title, and Steps) must be filled."

            entered_new_test_data = {
                Constants.TestEffortsDataJSON.TEST_ID: test_id_pattern,
                "test_name": test_name,
                "preconditions": preconditions_data,
                "steps": steps_and_expected_data,
                Constants.TestEffortsDataJSON.TEST_LEVEL: test_level,
                Constants.SuiteDataJSON.SUITE_NAME: str(suite_name)
                .split("(")[1]
                .rstrip(")"),
                Constants.ProjectDataJSON.PROJECT_NAME: str(project_name)
                .split("(")[1]
                .rstrip(")"),
            }

            data[test_id_pattern] = entered_new_test_data

            test_cases_mapper_instance.save_to_json_storage(data)

            # FileHandler.save_new_file(
            #     file_pathname=test_case_file_pathname, content=steps_and_expected_data
            # )

            return (
                html.Pre(f"Test Case saved successfully"),
                None,
            )
        case _:
            return "Please fill out the fields before submitting a test case", None


app.layout = html_register_feature_or_tests.render_layout()
