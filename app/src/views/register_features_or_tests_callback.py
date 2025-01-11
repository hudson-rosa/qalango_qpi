import dash
import json

from collections import Counter
from behave.parser import ParserError, parse_feature
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
    return Constants.FieldText.THIS_SCENARIO_TAKES_TIME.format(
        time=StringHandler.format_time_to_hh_mm(value)
    )


@callback(
    [
        Output({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "theme"),
        Output({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "className"),
    ],
    [
        Input({"type": "rsc--bdd-theme-button-a", "index": MATCH}, "n_clicks"),
        Input({"type": "rsc--bdd-theme-button-b", "index": MATCH}, "n_clicks"),
        Input({"type": "rsc--bdd-theme-button-c", "index": MATCH}, "n_clicks"),
        Input({"type": "rsc--bdd-theme-button-d", "index": MATCH}, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def bdd_editor_toggle_theme(n_clicks_a, n_clicks_b, n_clicks_c, n_clicks_d):
    ctx = dash.callback_context
    button_id = ValidationUtils.identify_triggering_action_on_nested_dict(
        callback_context=ctx
    )
    if button_id and "type" in button_id:
        match button_id["type"]:
            case "rsc--bdd-theme-button-a":
                return "dracula", "c_text_editor custom-theme"
            case "rsc--bdd-theme-button-b":
                return "twilight", ""
            case "rsc--bdd-theme-button-c":
                return "monokai", ""
            case "rsc--bdd-theme-button-d":
                return "github", ""

    return dash.no_update, dash.no_update


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
    [
        Output(
            {"type": "rsc--bdd-categories-checkbox-output", "index": MATCH}, "children"
        ),
        Output(
            {"type": "rsc--bdd-categories-checkbox-output", "index": MATCH}, "className"
        ),
    ],
    Input({"type": "rsc--bdd-categories-checkbox", "index": MATCH}, "value"),
)
def update_bdd_multi_checkbox_output(selected):
    if selected:
        return (
            f"{Constants.FieldText.CATEGORIES_SELECTED}: {', '.join(selected)}",
            "text-selected",
        )
    return Constants.FieldText.NO_OPTIONS_SELECTED, "no-text-selected"


@callback(
    Output({"type": "rsc--bdd-validation-output", "index": MATCH}, "children"),
    Output({"type": "rsc--bdd-validation-output", "index": MATCH}, "className"),
    [
        Input("rsc--bdd-feature-editor", "value"),
        Input({"type": "rsc--bdd-scenario-editor", "index": MATCH}, "value"),
    ],
)
def validate_gherkin(bdd_feature_content, gherkin_text):
    if not str(bdd_feature_content).strip() or not str(gherkin_text).strip():
        return (
            Constants.Messages.MISSING_FIELDS
            + Constants.Messages.PLEASE_ENTER_GHERKIN_CONTENT_WITH_KEYWORDS,
            "validation-error",
        )

    return ValidationUtils.validate_gherkin_syntax(
        f"{bdd_feature_content}\n{gherkin_text}"
    )


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
        State({"type": "rsc--bdd-requirements-link", "index": ALL}, "value"),
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
        State({"type": "rsc--bdd-categories-checkbox", "index": ALL}, "value"),
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
    requirements_link,
    bdd_scenarios,
    test_levels,
    test_approaches,
    test_durations,
    test_categories,
):
    ctx = dash.callback_context
    button_id = ValidationUtils.identify_triggering_action(callback_context=ctx)

    # Refresh Scenario ID if not loaded
    if feature_id is None:
        feature_id = idfeat_prefix + DataGenerator.generate_aggregated_uuid()

    # Validation Rules as tuples
    all_test_levels = [level for level in test_levels if level]
    validation_rules = [
        (not project_ref, Constants.Messages.PROJECT_REFERENCE_IS_REQUIRED),
        (not suite_ref, Constants.Messages.SUITE_REFERENCE_IS_REQUIRED),
        (not feature_name, Constants.Messages.FEATURE_NAME_IS_REQUIRED),
        (
            not bdd_feature_content,
            Constants.Messages.GHERKIN_FEATURE_CONTENT_IS_REQUIRED,
        ),
        (
            not bdd_scenarios or not all(bdd_scenarios),
            Constants.Messages.ALL_SCENARIOS_MUST_HAVE_GHERKIN_CONTENT,
        ),
        (
            not all_test_levels or len(all_test_levels) != len(bdd_scenarios),
            Constants.Messages.EACH_SCENARIO_MUST_HAVE_A_TEST_LEVEL,
        ),
        (
            not test_approaches or len(test_approaches) != len(bdd_scenarios),
            Constants.Messages.EACH_SCENARIO_MUST_HAVE_A_TEST_APPROACH,
        ),
    ]

    feature_name_underlined = str(feature_name).replace(" ", "_").strip()
    feature_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{feature_id}--{feature_name_underlined.lower()}.feature"

    match button_id:
        case "rsc--submit-bdd-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.BDD_FEATURE_FILE_PATHNAME_IS_SAVED.format(
                        feature_file_pathname=feature_file_pathname
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, None

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
                    "requirements_link": requirements_link[index],
                    "test_level": test_levels[index],
                    "test_approach": test_approaches[index],
                    "test_duration": test_durations[index],
                    "test_categories": test_categories[index],
                    "content": feature_file_pathname,
                }
                scenarios_data.append(scenario_data)

                # prepare data for .feature file
                normalized_tags = prepare_tags_for_feature_file(
                    test_levels,
                    test_approaches,
                    test_durations,
                    test_categories,
                    index,
                    scenario_id_tag,
                )
                bdd_content_lines.append(
                    f"\n\n{normalized_tags}\n{scenario_content.strip()}"
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
            test_category_smoke_tes_count = Counter(
                [
                    category
                    for sublist in test_categories
                    for category in sublist
                    if category == Constants.TestCategoriesEntity.SMOKE_TEST
                ]
            )
            test_category_edge_case_count = Counter(
                [
                    category
                    for sublist in test_categories
                    for category in sublist
                    if category == Constants.TestCategoriesEntity.EDGE_CASE
                ]
            )
            test_category_critical_test_count = Counter(
                [
                    category
                    for sublist in test_categories
                    for category in sublist
                    if category == Constants.TestCategoriesEntity.CRITICAL_TEST
                ]
            )
            test_category_mobile_count = Counter(
                [
                    category
                    for sublist in test_categories
                    for category in sublist
                    if category == Constants.TestCategoriesEntity.MOBILE
                ]
            )
            test_category_desktop_count = Counter(
                [
                    category
                    for sublist in test_categories
                    for category in sublist
                    if category == Constants.TestCategoriesEntity.DESKTOP
                ]
            )

            # prepare feature summary data
            new_scn_data = {
                Constants.FeaturesDataJSON.SPEC_DOC_ID: feature_id,
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
                "test_categories": {
                    Constants.FeaturesDataJSON.QTY_OF_CRITICAL_TESTS: test_category_critical_test_count.get(
                        Constants.TestCategoriesEntity.CRITICAL_TEST, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_SMOKE_TESTS: test_category_smoke_tes_count.get(
                        Constants.TestCategoriesEntity.SMOKE_TEST, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_EDGE_CASES: test_category_edge_case_count.get(
                        Constants.TestCategoriesEntity.EDGE_CASE, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_MOBILE: test_category_mobile_count.get(
                        Constants.TestCategoriesEntity.MOBILE, 0
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_DESKTOP: test_category_desktop_count.get(
                        Constants.TestCategoriesEntity.DESKTOP, 0
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

            data[project_id]["feature_specs"].append(new_scn_data)

            # Save to files
            scenarios_mapper_instance.save_to_json_storage(data)
            scenarios_mapper_instance.save_content_to_new_file(
                new_file=feature_file_pathname,
                new_data=aggregated_bdd_feature_content,
            )

            new_id = idfeat_prefix + DataGenerator.generate_aggregated_uuid()

            return (validation_message, new_id)

        case "rsc--delete-bdd-file-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.BDD_FEATURE_FILE_PATHNAME_IS_DELETED.format(
                        feature_file_pathname=feature_file_pathname
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, None

            try:
                data = scenarios_mapper_instance.load_from_json_storage()
                FileHandler.delete_file(feature_file_pathname)

                if feature_id in data:
                    del data[feature_id]
                    scenarios_mapper_instance.save_to_json_storage(data)
                    return (
                        validation_message,
                        None,
                    )
                else:
                    return (
                        None,
                        Constants.Messages.FEATURE_FILE_WAS_NOT_FOUND,
                    )
            except FileNotFoundError:
                return (
                    html.Pre(Constants.Messages.DELETION_FAILED_FEATURE_FILE_NOT_FOUND),
                    None,
                )

        case _:
            return (
                Constants.Messages.PLEASE_FILL_IN_THE_FIELDS_BEFORE_CHOOSING_AN_ACTION,
                None,
            )


def prepare_tags_for_feature_file(
    test_levels,
    test_approaches,
    test_durations,
    test_categories,
    index,
    scenario_id_tag,
):
    cov_test_level_tag = f"@track-{test_levels[index]}" if test_levels[index] else ""
    cov_test_approach_tag = (
        f"@track-{test_approaches[index]}" if test_approaches[index] else ""
    )
    cov_test_category_tags = (
        [
            f"@track-{categories_sublist}"
            for categories_sublist in test_categories[index]
        ]
        if test_categories is not None
        else ""
    )
    time_taken_tag = (
        f"@time-{test_durations[index]}m" if test_durations[index] else "@time-0m"
    )
    join_scenario_tags = f"{scenario_id_tag}{cov_test_level_tag}{cov_test_approach_tag}{cov_test_category_tags}{time_taken_tag}".replace(
        " ", ""
    )
    normalized_tags = (
        str(
            StringHandler.remove_brackets_quotes_and_commas_from_string(
                join_scenario_tags
            )
        )
        .replace("@", " @")
        .strip()
    )

    return normalized_tags


@callback(
    Output("rsc--tc-slider-output", "children"),
    Input("rsc--tc-total-time-slider", "value"),
)
def update_tc_slider_output(value):
    return Constants.FieldText.THIS_TEST_TAKES_TIME.format(
        time=StringHandler.format_time_to_hh_mm(value)
    )


@callback(
    [
        Output("rsc--tc-categories-checkbox-output", "children"),
        Output("rsc--tc-categories-checkbox-output", "className"),
    ],
    Input("rsc--tc-categories-checkbox", "value"),
)
def update_tc_multi_checkbox_output(selected):
    if selected:
        return (
            f"{Constants.FieldText.CATEGORIES_SELECTED}: {', '.join(selected)}",
            "text-selected",
        )
    return Constants.FieldText.NO_OPTIONS_SELECTED, "no-text-selected"


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
            placeholder=f"{Constants.FieldText.ENTER_PRECONDITION} {precond_block_number}",
            required=True,
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
            placeholder=f"{Constants.FieldText.ENTER_STEP} {step_block_number}",
            required=True,
        )
        new_expected = dcc.Textarea(
            id=f"rsc--expected-{step_block_number}",
            placeholder=f"{Constants.FieldText.ENTER_EXPECTED_RESULT} {step_block_number}",
            required=False,
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
        State("rsc--tc-requirements-link", "value"),
        State("rsc--tc-preconditions-container", "children"),
        State("rsc--tc-steps-container", "children"),
        State("rsc--tc-test-level-dropdown", "value"),
        State("rsc--tc-test-approach-radio", "value"),
        State("rsc--tc-total-time-slider", "value"),
        State("rsc--tc-categories-checkbox", "value"),
    ],
    prevent_initial_call="initial_duplicate",
)
def submit_scripted_test(
    submit_clicks,
    suite_ref,
    project_ref,
    test_id,
    test_name,
    requirements_link,
    preconditions_children,
    children_steps,
    test_level,
    test_approach,
    test_duration,
    test_categories,
):
    ctx = dash.callback_context
    button_id = ValidationUtils.identify_triggering_action(callback_context=ctx)

    # Refresh Test Case ID if not loaded
    if test_id is None:
        test_id = idtest_prefix + DataGenerator.generate_aggregated_uuid()

    # Validation Rules as tuples
    validation_rules = [
        (not project_ref, Constants.Messages.PROJECT_REFERENCE_IS_REQUIRED),
        (not suite_ref, Constants.Messages.SUITE_REFERENCE_IS_REQUIRED),
        (not test_name, Constants.Messages.TEST_NAME_IS_REQUIRED),
        (not test_level, Constants.Messages.TEST_LEVEL_IS_REQUIRED),
    ]

    match button_id:
        case "rsc--submit-tc-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.TEST_CASE_SCENARIO_IS_SAVED.format(
                        test_id=test_id
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, None

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

            # Preconditions and Step fields validation
            steps_validation_rules = [
                (
                    any(not p["precondition"] for p in preconditions_data),
                    Constants.Messages.ALL_ADDED_PRECONDITIONS_NEED_TO_BE_FILLED_IN,
                ),
                (
                    any(not s["step"] for s in steps_and_expected_data),
                    Constants.Messages.ALL_ADDED_STEPS_NEED_TO_BE_FILLED_IN,
                ),
            ]

            is_valid, steps_message = ValidationUtils.validate_mandatory_field_rules(
                Constants.Messages.TEST_CASE_STEPS_ARE_SAVED, steps_validation_rules
            )
            ## Steps field validation is disabled
            # if not is_valid:
            #     return steps_message, None

            project_id = StringHandler.get_id_format(project_ref)
            project_name = StringHandler.get_name_format(project_ref)
            suite_name = str(suite_ref).split("(")[0].strip()
            requirements_link = str(requirements_link).strip()

            scenario_data = {
                Constants.ScenariosDataJSON.SCENARIO_ID: test_id,
                Constants.ScenariosDataJSON.SCENARIO_NAME: test_name,
                Constants.FeaturesDataJSON.REQUIREMENTS_LINK: requirements_link,
                "test_level": test_level,
                "test_approach": test_approach,
                "test_categories": test_categories,
                "test_duration": test_duration,
                "content": {
                    "preconditions": preconditions_data,
                    "steps": steps_and_expected_data,
                },
            }

            try:
                data = scenarios_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            # prepare summary data
            new_test_data = {
                Constants.FeaturesDataJSON.SPEC_DOC_ID: test_id,
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
                "test_categories": {
                    Constants.FeaturesDataJSON.QTY_OF_CRITICAL_TESTS: int(
                        Constants.TestCategoriesEntity.CRITICAL_TEST in test_categories
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_SMOKE_TESTS: int(
                        Constants.TestCategoriesEntity.SMOKE_TEST in test_categories
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_EDGE_CASES: int(
                        Constants.TestCategoriesEntity.EDGE_CASE in test_categories
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_MOBILE: int(
                        Constants.TestCategoriesEntity.MOBILE in test_categories
                    ),
                    Constants.FeaturesDataJSON.QTY_OF_DESKTOP: int(
                        Constants.TestCategoriesEntity.DESKTOP in test_categories
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

            data[project_id]["feature_specs"].append(new_test_data)

            scenarios_mapper_instance.save_to_json_storage(data)

            new_id = idtest_prefix + DataGenerator.generate_aggregated_uuid()

            return (validation_message, new_id)
        case _:
            return (
                Constants.Messages.PLEASE_FILL_IN_THE_FIELDS_BEFORE_CHOOSING_AN_ACTION,
                None,
            )


app.layout = html_register_feature_or_tests.render_layout()
