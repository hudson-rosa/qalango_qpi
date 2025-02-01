from dash import dcc, html
from dash_ace import DashAceEditor

from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.suite_mapper import SuiteMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants
from src.utils.data_generator import DataGenerator

def render_layout():
    return html.Div(
        [
            html.Title("Test"),
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.FEATURES
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.FEATURES
            ),
            html.Div(
                className="form-content",
                children=[
                    html.Div(
                        className="toggle-container",
                        children=[
                            html.Button(
                                Constants.FieldText.BDD_SCENARIO_FORMAT,
                                id="rsc--toggle-bdd",
                                n_clicks=0,
                                className="toggle-btn active",
                            ),
                            html.Button(
                                "Scripted Test format",
                                id="rsc--toggle-tc",
                                n_clicks=0,
                                className="toggle-btn",
                            ),
                        ],
                    ),
                    html.Div(
                        className="section-group",
                        children=[
                            generate_new_id(),
                            define_project_and_suite(),
                        ],
                    ),
                    register_bdd_feature_scenarios(),
                    register_scripted_test_cases(),
                ],
            ),
        ]
    )


def generate_new_id():
    return html.Div(
        className="grid-2",
        children=[
            dcc.Input(
                id="rsc--feature-or-test-id",
                type="text",
                placeholder=Constants.FieldText.FEATURE_ID,
                required=True,
                readOnly=True,
                className="inline-grid",
            ),
            html.Button(
                Constants.FieldText.GENERATE_NEW_ID,
                id="rsc--generate-id-button",
                className="inline-grid",
            ),
        ],
    )


def define_project_and_suite():
    return html.Div(
        className="grid grid-2",
        children=[
            dcc.Dropdown(
                id="rsc--project-dropdown",
                options=ProjectMapper.get_project_options(),
                placeholder=Constants.FieldText.SELECT_PROJECT_NAME,
                searchable=True,
                className="c_dropdown required",
            ),
            dcc.Dropdown(
                id="rsc--suite-dropdown",
                options=SuiteMapper.get_suite_options(),
                placeholder=Constants.FieldText.SELECT_SUITE_NAME,
                searchable=True,
                className="c_dropdown required",
            ),
        ],
    )


def register_bdd_feature_scenarios():
    return html.Div(
        id="rsc--bdd-container",
        children=[
            html.Ul(
                html.Li(
                    html.Div(
                        className="section-group",
                        children=[
                            dcc.Input(
                                id="rsc--bdd-feature-name",
                                type="text",
                                placeholder=Constants.FieldText.ENTER_FEATURE_NAME,
                                required=True,
                            ),
                        ],
                    )
                ),
            ),
            html.Div(
                className="section-group",
                children=[
                    html.H3(Constants.FieldText.ENTER_YOUR_GHERKIN_FEATURE),
                    dcc.Textarea(
                        id="rsc--bdd-feature-editor",
                        style={"height": "200px !important"},
                        placeholder=Constants.FieldText.EG_FEATURE_USER_LOGIN,
                        required=True,
                    ),
                ],
            ),
            # =========================
            define_bdd_scenario_details(scenario_id_suffix=1),
            # =========================
            html.Button(
                Constants.FieldText.ADD_NEW_SCENARIO,
                id="rsc--bdd-add-scenario-button",
                n_clicks=0,
                className="add-scenario-btn",
            ),
            html.Label(Constants.FieldText.REQUIRED_FIELDS, className="required-msg"),
            html.Div(
                id="rsc--bdd-output-message",
                className="output-msg",
            ),
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                Constants.FieldText.SAVE_FEATURE,
                                id="rsc--submit-bdd-button",
                                n_clicks=0,
                                className="submit-btn",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                Constants.FieldText.DELETE_FILE,
                                id="rsc--delete-bdd-file-button",
                                n_clicks=0,
                            ),
                        ]
                    ),
                ],
            ),
        ],
        style={"display": "block"},
    )


def define_bdd_scenario_details(scenario_id_suffix=1):
    return html.Div(
        id="rsc--bdd-scenarios-container",
        children=[
            html.Hr(),
            html.H3(
                f"{Constants.FieldText.ENTER_YOUR_GHERKIN_SCENARIO} {scenario_id_suffix}"
            ),
            html.Div(
                className="grid",
                children=[
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Div(
                                [
                                    html.H4(
                                        Constants.FieldText.CHOOSE_TEST_LEVEL_APPROACH
                                    ),
                                    dcc.Dropdown(
                                        options=TestEffortsMapper.get_list_of_test_levels(),
                                        id={
                                            "type": "rsc--bdd-test-level-dropdown",
                                            "index": scenario_id_suffix,
                                        },
                                        placeholder=Constants.FieldText.ENTER_SCENARIO_LEVEL,
                                        searchable=True,
                                        className=" c_dropdown required",
                                        value=None,
                                    ),
                                    html.Div(
                                        children=[
                                            html.H4(
                                                Constants.FieldText.SELECT_TEST_APPROACH_FOR_THIS_SCENARIO
                                            ),
                                            dcc.RadioItems(
                                                id={
                                                    "type": "rsc--bdd-test-approach-radio",
                                                    "index": scenario_id_suffix,
                                                },
                                                options=[
                                                    {
                                                        "label": "Manual",
                                                        "value": Constants.TestTypesEntity.MANUAL,
                                                    },
                                                    {
                                                        "label": "Automated",
                                                        "value": Constants.TestTypesEntity.AUTOMATED,
                                                    },
                                                ],
                                                className="c_radio",
                                                value=Constants.TestTypesEntity.MANUAL,
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            html.Div(
                                [
                                    html.H4(Constants.FieldText.CHOOSE_TEST_CATEGORY),
                                    dcc.Checklist(
                                        id={
                                            "type": "rsc--bdd-categories-checkbox",
                                            "index": scenario_id_suffix,
                                        },
                                        options=TestEffortsMapper.get_list_of_test_categories(),
                                        value=[],
                                        className="c_check",
                                    ),
                                    html.H5(
                                        id={
                                            "type": "rsc--bdd-categories-checkbox-output",
                                            "index": scenario_id_suffix,
                                        }
                                    ),
                                    html.H4(
                                        Constants.FieldText.ENTER_AVERAGE_TEST_EXECUTION_DURATION
                                    ),
                                    dcc.Slider(
                                        id={
                                            "name": "rsc--bdd-total-time-scenario-slider",
                                            "type": "slider",
                                            "index": scenario_id_suffix,
                                        },
                                        min=0,
                                        max=181,
                                        marks=DataGenerator.generate_slider_marks(),
                                        step=None,
                                        value=0,
                                        included=False,
                                        tooltip={
                                            "placement": "bottom",
                                            "always_visible": True,
                                        },
                                        className="c_slider",
                                    ),
                                    html.H5(
                                        id={
                                            "name": "rsc--bdd-slider-output",
                                            "type": "slider-output",
                                            "index": scenario_id_suffix,
                                        },
                                    ),
                                ]
                            ),
                        ],
                    ),
                    dcc.Input(
                        id={
                            "type": "rsc--bdd-requirements-link",
                            "index": scenario_id_suffix,
                        },
                        type="text",
                        placeholder=Constants.FieldText.REQUIREMENTS_LINK,
                        required=False,
                    ),
                ],
            ),
            html.Div(
                id={
                    "type": "rsc--bdd-scenario-editor-container",
                    "index": scenario_id_suffix,
                },
                className="section-group",
                children=[
                    DashAceEditor(
                        id={
                            "type": "rsc--bdd-scenario-editor",
                            "index": scenario_id_suffix,
                        },
                        theme="twilight",  # e.g., monokai, twilight, solarized_dark
                        mode="gherkin",
                        className="c_text_editor custom-theme",
                        style={"min-height": "200px !important", "width": "100%"},
                        enableBasicAutocompletion=True,
                        enableSnippets=True,
                        enableLiveAutocompletion=True,
                        showPrintMargin=True,
                        value=f"""Scenario: Successful login (Example #{scenario_id_suffix})
    Given the user is on the login page
    When they enter valid credentials
    Then they should be redirected to the dashboard
    """,
                    ),
                    html.Div(
                        className="editor-buttons",
                        children=[
                            html.H4(
                                "Themes: ",
                                id={
                                    "type": "rsc--bdd-theme-label",
                                    "index": scenario_id_suffix,
                                },
                                className="change-theme-label",
                            ),
                            html.Button(
                                "Default",
                                id={
                                    "type": "rsc--bdd-theme-button-a",
                                    "index": scenario_id_suffix,
                                },
                                className="change-theme-button",
                            ),
                            html.Button(
                                "Twilight",
                                id={
                                    "type": "rsc--bdd-theme-button-b",
                                    "index": scenario_id_suffix,
                                },
                                className="change-theme-button",
                            ),
                            html.Button(
                                "Monokai",
                                id={
                                    "type": "rsc--bdd-theme-button-c",
                                    "index": scenario_id_suffix,
                                },
                                className="change-theme-button",
                            ),
                            html.Button(
                                "GitHub",
                                id={
                                    "type": "rsc--bdd-theme-button-d",
                                    "index": scenario_id_suffix,
                                },
                                className="change-theme-button",
                            ),
                        ],
                    ),
                    html.Div(
                        id={
                            "type": "rsc--bdd-validation-output",
                            "index": scenario_id_suffix,
                        },
                        className="output-msg",
                    ),
                ],
            ),
        ],
    )


def register_scripted_test_cases():
    return html.Div(
        id="rsc--tc-container",
        className="section-group",
        children=[
            dcc.Input(
                id="rsc--tc-test-name",
                type="text",
                placeholder=Constants.FieldText.ENTER_TEST_CASE_TITLE_OR_OBJECTIVE,
                required=True,
            ),
            dcc.Input(
                id="rsc--tc-requirements-link",
                type="text",
                placeholder=Constants.FieldText.REQUIREMENTS_LINK,
                required=False,
            ),
            # =========================
            define_test_case_details(),
            # =========================
            html.H3(Constants.FieldText.ENTER_PRECONDITIONS_FOR_THIS_TEST_CASE),
            html.Div(
                id="rsc--tc-preconditions-container",
                children=[
                    dcc.Textarea(
                        id="rsc--precondition-1",
                        placeholder=Constants.FieldText.ENTER_PRECONDITION + " 1",
                        required=True,
                    )
                ],
            ),
            html.Button(
                Constants.FieldText.ADD_PRECONDITION,
                id="rsc--tc-add-precondition",
                n_clicks=0,
                className="add-precondition-btn",
            ),
            html.H3(Constants.FieldText.ENTER_TEST_CASE_STEPS_AND_EXPECTED_RESULTS),
            html.Div(
                id="rsc--tc-steps-container",
                className="grid grid-2",
                children=[
                    dcc.Textarea(
                        id="rsc--step-1",
                        placeholder=Constants.FieldText.ENTER_STEP + " 1",
                        required=True,
                        style={"height": "500px !important"},
                    ),
                    dcc.Textarea(
                        id="rsc--expected-1",
                        placeholder=Constants.FieldText.ENTER_EXPECTED_RESULT + " 1",
                        style={"height": "500px !important"},
                    ),
                ],
            ),
            html.Button(
                Constants.FieldText.ADD_STEP,
                id="rsc--tc-add-step-button",
                n_clicks=0,
                className="add-btn",
            ),
            html.Label(Constants.FieldText.REQUIRED_FIELDS, className="required-msg"),
            html.Div(
                id="rsc--tc-output-message",
                className="output-msg",
            ),
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                Constants.FieldText.SAVE_NEW_TEST_CASE,
                                id="rsc--submit-tc-button",
                                n_clicks=0,
                                className="submit-btn",
                            ),
                        ]
                    ),
                ],
            ),
        ],
        style={"display": "none"},
    )


def define_test_case_details(scenario_id_suffix=1):
    return html.Div(
        className="grid",
        children=[
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        [
                            html.H4(Constants.FieldText.CHOOSE_TEST_LEVEL_APPROACH),
                            dcc.Dropdown(
                                options=TestEffortsMapper.get_list_of_test_levels(),
                                id="rsc--tc-test-level-dropdown",
                                placeholder=Constants.FieldText.ENTER_TEST_LEVEL,
                                searchable=True,
                                className=" c_dropdown required",
                                value="",
                            ),
                            html.Div(
                                children=[
                                    html.H4(Constants.FieldText.SELECT_TEST_APPROACH),
                                    dcc.RadioItems(
                                        id="rsc--tc-test-approach-radio",
                                        options=[
                                            {
                                                "label": "Manual",
                                                "value": Constants.TestTypesEntity.MANUAL,
                                            },
                                            {
                                                "label": "Automated",
                                                "value": Constants.TestTypesEntity.AUTOMATED,
                                            },
                                        ],
                                        className="c_radio",
                                        value=Constants.TestTypesEntity.MANUAL,
                                    ),
                                ]
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.H4(Constants.FieldText.CHOOSE_TEST_CATEGORY),
                            dcc.Checklist(
                                id="rsc--tc-categories-checkbox",
                                options=TestEffortsMapper.get_list_of_test_categories(),
                                value=[],
                                className="c_check",
                            ),
                            html.H5(
                                id="rsc--tc-categories-checkbox-output",
                                className="no-text-selected",
                            ),
                            html.H4(
                                Constants.FieldText.ENTER_AVERAGE_TEST_EXECUTION_DURATION
                            ),
                            dcc.Slider(
                                id="rsc--tc-total-time-slider",
                                min=0,
                                max=181,
                                marks=DataGenerator.generate_slider_marks(),
                                step=None,
                                value=0,
                                included=False,
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                                className="c_slider",
                            ),
                            html.H5(id="rsc--tc-slider-output"),
                        ]
                    ),
                ],
            )
        ],
    )
