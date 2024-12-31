import dash
import json

from collections import Counter
from dash import dcc, callback, html, Input, Output, State, MATCH, ALL
from src.models.mapper.data_mapper import DataMapper
from src.models.mapper.suite_mapper import SuiteMapper

import src.views.layout.html_register_feature_or_tests as html_register_feature_or_tests
from src.utils.data_generator import DataGenerator
from src.utils.file_handler import FileHandler
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils
from src.utils.string_handler import StringHandler


app = dash.Dash(__name__)
ctx = dash.callback_context
slider_marks = DataGenerator.generate_slider_marks()

scenarios_json_storage = Constants.FilePaths.SCENARIOS_DATA_JSON_PATH
scenarios_mapper_instance = DataMapper(filename=scenarios_json_storage)

idfeat_prefix = "idbdd_"
idtest_prefix = "idtest_"


def is_matching_test_level(current_test_level, expected=""):
    return int(current_test_level == expected)


@callback(
    Output("rsc--feature-or-test-id", "value"),
    [
        Input("rsc--bdd-container", "style"),
        Input("rsc--tc-container", "style"),
        Input("rsc--generate-id-button", "n_clicks"),
    ],
    prevent_initial_call=False,
)
def update_random_id(bdd_style, tc_style, n_clicks):
    if bdd_style.get("display") == "block":
        prefix = idfeat_prefix
    elif tc_style.get("display") == "block":
        prefix = idtest_prefix
    else:
        prefix = "unknown_"

    return prefix + DataGenerator.generate_aggregated_uuid()


@callback(
    Output("rsc--suite-dropdown", "options"), [Input("rsc--project-dropdown", "value")]
)
def update_suite_options(selected_project):
    if not selected_project:
        return []
    project_id = StringHandler.get_id_format(selected_project)
    return SuiteMapper.get_suite_options(project_id=project_id)


@callback(
    [
        Output("rsc--bdd-container", "style"),
        Output("rsc--tc-container", "style"),
        Output("rsc--toggle-bdd", "className"),
        Output("rsc--toggle-tc", "className"),
    ],
    [Input("rsc--toggle-bdd", "n_clicks"), Input("rsc--toggle-tc", "n_clicks")],
)
def toggle_form(bdd_clicks, tc_clicks):
    bdd_toggle_style = {"display": "block"}
    tc_toggle_style = {"display": "none"}
    bdd_class = "toggle-btn active"
    tc_class = "toggle-btn"

    if ctx.triggered_id == "rsc--toggle-tc":
        bdd_toggle_style = {"display": "none"}
        tc_toggle_style = {"display": "block"}
        bdd_class = "toggle-btn"
        tc_class = "toggle-btn active"

    return bdd_toggle_style, tc_toggle_style, bdd_class, tc_class


@callback(
    Output(
        {"type": "slider-output", "index": MATCH, "name": "rsc--bdd-slider-output"},
        "children",
    ),
    Input(
        {
            "type": "slider",
            "index": MATCH,
            "name": "rsc--bdd-total-time-scenario-slider",
        },
        "value",
    ),
)
def update_bdd_slider_output(value):
    return "This scenario takes " + StringHandler.format_time_to_hh_mm(value)


@callback(
    Output({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "style"),
    Input({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "value"),
    State({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "style"),
)
def auto_resize_textarea(content, current_style):
    if content:
        line_count = str(content).count("\n") + 1
        new_dynamic_height = min(150 + line_count * 20, 800)
        updated_style = {**current_style, "height": f"{new_dynamic_height}px"}
        return updated_style
    return current_style


@callback(
    Output("rsc--bdd-scenarios-container", "children"),
    Input("rsc--bdd-add-scenario-button", "n_clicks"),
    State("rsc--bdd-scenarios-container", "children"),
    prevent_initial_call=True,
)
def add_all_bdd_scenario_fields(n_clicks, current_children):
    if current_children is None:
        current_children = []

    if n_clicks is None:
        return current_children

    scenario_id_suffix = n_clicks + 1

    new_scenario_block = html_register_feature_or_tests.define_bdd_scenario_details(
        scenario_id_suffix=scenario_id_suffix
    )

    return current_children + [new_scenario_block]


@callback(
    [
        Output("rsc--bdd-output-message", "children"),
        Output("rsc--feature-or-test-id", "value", allow_duplicate=True),
    ],
    [
        Input("rsc--submit-bdd-button", "n_clicks"),
        Input("rsc--delete-bdd-file-button", "n_clicks"),
    ],
    [
        State("rsc--suite-dropdown", "value"),
        State("rsc--project-dropdown", "value"),
        State("rsc--feature-or-test-id", "value"),
        State("rsc--bdd-feature-name", "value"),
        State("rsc--bdd-feature-editor", "value"),
        State({"type": "rsc--bdd-scenario-editor", "index": ALL}, "value"),
        State({"type": "rsc--bdd-test-level-dropdown", "index": ALL}, "value"),
        State({"type": "rsc--bdd-test-approach-radio", "index": ALL}, "value"),
        State(
            {
                "type": "slider",
                "name": "rsc--bdd-total-time-scenario-slider",
                "index": ALL,
            },
            "value",
        ),
    ],
    prevent_initial_call="initial_duplicate",
)
def submit_bdd_data(
    submit_clicks,
    delete_file_clicks,
    suite_ref,
    project_ref,
    feature_id,
    feature_name,
    bdd_feature_content,
    bdd_scenarios,
    test_levels,
    test_approaches,
    test_durations,
):
    ctx = dash.callback_context

    # Identify the triggering input
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    # Validation Rules as tuples
    validation_rules = [
        (not project_ref, "- Project reference is required."),
        (not suite_ref, "- Suite reference is required."),
        (not feature_name, "- Feature Name is required."),
        (not bdd_feature_content, "- Gherkin Feature content is required."),
        (
            not bdd_scenarios or not all(bdd_scenarios),
            "- All scenarios must have Gherkin content.",
        ),
        (
            not test_levels or len(test_levels) != len(bdd_scenarios),
            "- Each scenario must have a test level.",
        ),
        (
            not test_approaches or len(test_approaches) != len(bdd_scenarios),
            "- Each scenario must have a test approach.",
        ),
        (
            not test_durations or len(test_durations) != len(bdd_scenarios),
            "- Each scenario must have a test duration.",
        ),
    ]
    error_message = ValidationUtils.validate_mandatory_field_rules(validation_rules)
    if error_message:
        return error_message, None

    feature_name_underlined = str(feature_name).replace(" ", "_").strip()
    feature_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{feature_id}--{feature_name_underlined.lower()}.feature"

    match button_id:
        case "rsc--submit-bdd-button":

            project_id = StringHandler.get_id_format(project_ref)
            suite_name = str(suite_ref).split("(")[0].strip()

            scenarios_data = []
            bdd_content_lines = [bdd_feature_content]

            # prepare scenarios data
            for index, scenario_content in enumerate(bdd_scenarios):
                base_feature_id = str(feature_id).replace(idfeat_prefix, "idscn_")
                scenario_id_tag = f"@{base_feature_id}-{index+1}"

                scenario_data = {
                    "scenario_id": scenario_id_tag,
                    "scenario_name": scenario_content.split("\n", 1)[0]
                    .replace("Scenario:", "")
                    .replace("Scenario Outline:", "")
                    .strip(),
                    "test_level": test_levels[index],
                    "test_approach": test_approaches[index],
                    "test_duration": test_durations[index],
                }
                scenarios_data.append(scenario_data)

                # prepare data for .feature file
                cov_test_level_tag = (
                    f"@cov-{test_levels[index]}" if test_levels[index] else ""
                )
                cov_test_approach_tag = (
                    f"@cov-{test_approaches[index]}" if test_approaches[index] else ""
                )
                time_taken_tag = (
                    f"@time-{test_durations[index]}m" if test_durations[index] else ""
                )
                join_scenario_tags = f"{scenario_id_tag} {cov_test_level_tag} {cov_test_approach_tag} {time_taken_tag}".strip()
                bdd_content_lines.append(
                    f"\n\n{join_scenario_tags}\n{scenario_content.strip()}"
                )

            aggregated_bdd_feature_content = "\n".join(bdd_content_lines)
            all_scenarios = aggregated_bdd_feature_content.lower()

            try:
                data = scenarios_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            # prepare feature summary data
            test_levels_count = Counter(test_levels)
            test_approaches_count = Counter(test_approaches)
            new_data = {
                Constants.FeaturesDataJSON.FEATURE_ID: feature_id,
                Constants.FeaturesDataJSON.FEATURE_NAME: feature_name_underlined,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: all_scenarios.count(
                    "scenario:"
                )
                + all_scenarios.count("scenario outline:"),
                "test_levels": {
                    Constants.FeaturesDataJSON.QTY_OF_INTEGRATION: test_levels_count.get(
                        Constants.TestLevelsEntity.INTEGRATION, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_COMPONENT: test_levels_count.get(
                        Constants.TestLevelsEntity.COMPONENT, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_CONTRACT: test_levels_count.get(
                        Constants.TestLevelsEntity.CONTRACT, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_API: test_levels_count.get(
                        Constants.TestLevelsEntity.API, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_E2E: test_levels_count.get(
                        Constants.TestLevelsEntity.E2E, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE: test_levels_count.get(
                        Constants.TestLevelsEntity.PERFORMANCE, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_SECURITY: test_levels_count.get(
                        Constants.TestLevelsEntity.SECURITY, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_USABILITY: test_levels_count.get(
                        Constants.TestLevelsEntity.USABILITY, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY: test_levels_count.get(
                        Constants.TestLevelsEntity.EXPLORATORY, 0
                    ),
                },
                "test_approaches": {
                    Constants.FeaturesDataJSON.QTY_OF_AUTOMATED: test_approaches_count.get(
                        Constants.TestTypesEntity.AUTOMATED, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_MANUAL: test_approaches_count.get(
                        Constants.TestTypesEntity.MANUAL, 0
                    ),
                },
                "scenarios": scenarios_data,
            }

            # Update the project data
            if project_id not in data:
                data[project_id] = {
                    Constants.ProjectDataJSON.PROJECT_NAME: project_ref,
                    Constants.SuiteDataJSON.SUITE_REF: suite_ref,
                    "feature_specs": [],
                }

            data[project_id]["feature_specs"].append(new_data)

            # Save to files
            scenarios_mapper_instance.save_to_json_storage(data)
            scenarios_mapper_instance.save_content_to_new_file(
                new_file=feature_file_pathname,
                new_data=aggregated_bdd_feature_content,
            )

            new_id = idfeat_prefix + DataGenerator.generate_aggregated_uuid()

            return (
                html.Pre(f"BDD Feature saved successfully:\n\n{feature_file_pathname}"),
                new_id,
            )

        case "rsc--delete-bdd-file-button":
            try:
                data = scenarios_mapper_instance.load_from_json_storage()
                FileHandler.delete_file(feature_file_pathname)

                if feature_id in data:
                    del data[feature_id]
                    scenarios_mapper_instance.save_to_json_storage(data)
                    return (
                        html.Pre(
                            f"Feature file deleted successfully:\n\n{feature_file_pathname}"
                        ),
                        None,
                    )
                else:
                    return (
                        None,
                        f"Feature file was not found",
                    )
            except FileNotFoundError:
                return (
                    html.Pre("Feature file not found. Deletion of JSON file failed."),
                    None,
                )

        case _:
            return "Please fill out the fields before submitting a feature file", None


@callback(
    Output("rsc--tc-slider-output", "children"),
    Input("rsc--tc-total-time-slider", "value"),
)
def update_tc_slider_output(value):
    return "This test takes " + StringHandler.format_time_to_hh_mm(value)


@callback(
    Output("rsc--tc-preconditions-container", "children"),
    Input("rsc--tc-add-precondition", "n_clicks"),
    State("rsc--tc-preconditions-container", "children"),
)
def add_test_precondition(n_clicks, existing_preconditions):
    if n_clicks > 0:
        precond_block_number = (len(existing_preconditions)) + 1

        new_precondition = dcc.Textarea(
            id=f"rsc--precondition-{precond_block_number}",
            placeholder=f"Enter precondition {precond_block_number}",
        )
        return existing_preconditions + [new_precondition]

    return existing_preconditions


@callback(
    Output("rsc--tc-steps-container", "children"),
    Input("rsc--tc-add-step-button", "n_clicks"),
    State("rsc--tc-steps-container", "children"),
)
def add_test_step(n_clicks, existing_steps):
    if n_clicks > 0:
        step_block_number = (len(existing_steps) // 2) + 1

        new_step = dcc.Textarea(
            id=f"rsc--step-{step_block_number}",
            placeholder=f"Enter step {step_block_number}",
        )
        new_expected = dcc.Textarea(
            id=f"rsc--expected-{step_block_number}",
            placeholder=f"Enter expected result {step_block_number}",
        )
        return existing_steps + [new_step, new_expected]

    return existing_steps


@callback(
    [
        Output("rsc--tc-output-message", "children"),
        Output("rsc--feature-or-test-id", "value", allow_duplicate=True),
    ],
    Input("rsc--submit-tc-button", "n_clicks"),
    [
        State("rsc--suite-dropdown", "value"),
        State("rsc--project-dropdown", "value"),
        State("rsc--feature-or-test-id", "value"),
        State("rsc--tc-test-name", "value"),
        State("rsc--tc-preconditions-container", "children"),
        State("rsc--tc-steps-container", "children"),
        State("rsc--tc-test-level-dropdown", "value"),
        State("rsc--tc-test-approach-radio", "value"),
        State("rsc--tc-total-time-slider", "value"),
    ],
    prevent_initial_call="initial_duplicate",
)
def submit_scripted_test(
    submit_clicks,
    suite_ref,
    project_ref,
    test_id,
    test_name,
    preconditions_children,
    children_steps,
    test_level,
    test_approach,
    test_duration,
):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    # Validation Rules as tuples
    validation_rules = [
        (not project_ref, "- Project reference is required."),
        (not suite_ref, "- Suite reference is required."),
        (not test_name, "- Test Name is required."),
        (not test_level, "- Test Level is required."),
        (
            not preconditions_children or len(preconditions_children) == 0,
            "- All Preconditions must have a content.",
        ),
        (
            not children_steps or len(children_steps) == 0,
            "- Each Test Case Step must have a content.",
        ),
    ]
    error_message = ValidationUtils.validate_mandatory_field_rules(validation_rules)
    if error_message:
        return error_message, None

    match button_id:
        case "rsc--submit-tc-button":
            # prepare test case data
            preconditions_data = []
            for i in range(0, len(preconditions_children), 2):
                precond_textarea = preconditions_children[i]
                step_value = precond_textarea.get("props", {}).get("value", "").strip()

                preconditions_data.append({"precondition": step_value})

            steps_and_expected_data = []
            for i in range(0, len(children_steps), 2):
                step_textarea = children_steps[i]
                expected_textarea = children_steps[i + 1]

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

            project_id = StringHandler.get_id_format(project_ref)
            project_name = StringHandler.get_name_format(project_ref)
            suite_name = str(suite_ref).split("(")[0].strip()

            scenario_data = {
                "test_content": {
                    Constants.ScenariosDataJSON.SCENARIO_ID: test_id,
                    Constants.ScenariosDataJSON.SCENARIO_NAME: test_name,
                    "test_level": test_level,
                    "test_approach": test_approach,
                    "test_duration": test_duration,
                    "preconditions": preconditions_data,
                    "steps": steps_and_expected_data,
                }
            }

            try:
                data = scenarios_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            # prepare feature summary data
            new_data = {
                Constants.ScenariosDataJSON.TEST_ID: test_id,
                Constants.ScenariosDataJSON.TEST_NAME: test_name,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: 1,
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
                "scenarios": scenario_data,
            }

            if project_id not in data:
                data[project_id] = {
                    Constants.ProjectDataJSON.PROJECT_NAME: project_name,
                    Constants.SuiteDataJSON.SUITE_REF: suite_ref,
                    "feature_specs": [],
                }

            data[project_id]["feature_specs"].append(new_data)

            scenarios_mapper_instance.save_to_json_storage(data)

            new_id = idtest_prefix + DataGenerator.generate_aggregated_uuid()

            return (
                html.Pre(f"Test Case saved successfully"),
                new_id,
            )
        case _:
            return "Please fill out the fields before submitting a test case", None


app.layout = html_register_feature_or_tests.render_layout()
