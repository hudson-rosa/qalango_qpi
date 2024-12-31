from dash import dcc, html

from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.suite_mapper import SuiteMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants
from src.utils.data_generator import DataGenerator


def render_layout():
    return html.Div(
        [
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
                                "BDD Scenario format",
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
                placeholder="Feature id",
                required=True,
                readOnly=True,
                className="inline-grid",
            ),
            html.Button(
                "Generate new ID",
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
                placeholder="Select project name",
                searchable=True,
                className="c_dropdown",
            ),
            dcc.Dropdown(
                id="rsc--suite-dropdown",
                options=SuiteMapper.get_suite_options(),
                placeholder="Select suite name",
                searchable=True,
                className="c_dropdown",
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
                                placeholder="Enter feature name",
                                required=True,
                            ),
                        ],
                    )
                ),
            ),
            html.Div(
                className="section-group",
                children=[
                    html.H3("Enter your Gherkin Feature"),
                    dcc.Textarea(
                        id="rsc--bdd-feature-editor",
                        style={"height": "200px !important"},
                        placeholder="E.g., Feature: User Login",
                    ),
                ],
            ),
            # =========================
            define_bdd_scenario_details(scenario_id_suffix=1),
            # =========================
            html.Button(
                "+ Add New Scenario",
                id="rsc--bdd-add-scenario-button",
                n_clicks=0,
                className="add-scenario-btn",
            ),
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
                                "Save feature",
                                id="rsc--submit-bdd-button",
                                n_clicks=0,
                                className="submit-btn",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                "Delete File",
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
            html.H3(f"Enter your Gherkin Scenario {scenario_id_suffix}"),
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        children=[
                            html.H4(
                                "Choose the test level/approach for coverage purposes."
                            ),
                            dcc.Dropdown(
                                options=TestEffortsMapper.get_list_of_test_levels(),
                                id={
                                    "type": "rsc--bdd-test-level-dropdown",
                                    "index": scenario_id_suffix,
                                },
                                placeholder="Enter scenario level",
                                searchable=True,
                                className="c_dropdown",
                                value="exploratory",
                            ),
                            html.H4(
                                "Enter the average test execution duration (HH:mm)"
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
                    html.Div(
                        children=[
                            html.H4("Select the test approach for this scenario"),
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
                id={
                    "type": "rsc--bdd-scenario-editor-container",
                    "index": scenario_id_suffix,
                },
                className="section-group",
                children=[
                    dcc.Textarea(
                        id={
                            "type": "rsc--bdd-scenario-editor",
                            "index": scenario_id_suffix,
                        },
                        style={"height": "600px !important"},
                        placeholder=f"""Scenario: Successful login (Example #{scenario_id_suffix})
    Given the user is on the login page
    When they enter valid credentials
    Then they should be redirected to the dashboard
    """,
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
                placeholder="Enter test case title or objective",
                required=True,
            ),
            # =========================
            define_test_case_details(),
            # =========================
            html.H3("Enter the Preconditions for this Test Case"),
            html.Div(
                id="rsc--tc-preconditions-container",
                children=[
                    dcc.Textarea(
                        id="rsc--precondition-1",
                        placeholder="Enter precondition 1",
                        required=True,
                    )
                ],
            ),
            html.Button(
                "+ Add Precondition",
                id="rsc--tc-add-precondition",
                n_clicks=0,
                className="add-precondition-btn",
            ),
            html.H3("Enter the Test Case steps and expected results"),
            html.Div(
                id="rsc--tc-steps-container",
                className="grid grid-2",
                children=[
                    dcc.Textarea(
                        id="rsc--step-1",
                        placeholder="Enter step 1",
                        required=True,
                        style={"height": "500px !important"},
                    ),
                    dcc.Textarea(
                        id="rsc--expected-1",
                        placeholder="Enter expected result 1",
                        required=True,
                        style={"height": "500px !important"},
                    ),
                ],
            ),
            html.Button(
                "+ Add Step",
                id="rsc--tc-add-step-button",
                n_clicks=0,
                className="add-btn",
            ),
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
                                "Save new test",
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
        className="grid grid-2",
        children=[
            html.Div(
                [
                    html.H4("Choose the test level/approach for coverage purposes."),
                    dcc.Dropdown(
                        options=TestEffortsMapper.get_list_of_test_levels(),
                        id="rsc--tc-test-level-dropdown",
                        placeholder="Enter test level",
                        searchable=True,
                        className="c_dropdown",
                        value="exploratory",
                    ),
                    html.H4("Enter the average test execution duration (HH:mm)"),
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
            html.Div(
                [
                    html.H4("Selected the test approach"),
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
    )
