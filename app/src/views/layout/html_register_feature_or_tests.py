from dash import dcc, html

from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.suite_mapper import SuiteMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


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
                                id="rf--toggle-bdd",
                                n_clicks=0,
                                className="toggle-btn active",
                            ),
                            html.Button(
                                "Scripted Test format",
                                id="rf--toggle-scripted",
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
                id="rf--feature-or-test-id",
                type="text",
                placeholder="Feature id",
                required=True,
                readOnly=True,
                className="inline-grid",
            ),
            html.Button(
                "Generate new ID",
                id="rf--generate-id-button",
                className="inline-grid",
            ),
        ],
    )


def define_project_and_suite():
    return html.Div(
        className="grid grid-2",
        children=[
            dcc.Dropdown(
                id="rf--project-dropdown",
                options=ProjectMapper.get_project_options(),
                placeholder="Select project name",
                searchable=True,
                className="c_dropdown",
            ),
            dcc.Dropdown(
                id="rf--suite-dropdown",
                options=SuiteMapper.get_suite_options(),
                placeholder="Select suite name",
                searchable=True,
                className="c_dropdown",
            ),
        ],
    )


def register_bdd_feature_scenarios():
    return html.Div(
        id="rf--bdd-container",
        children=[
            html.Ul(
                html.Li(
                    html.Div(
                        className="section-group",
                        children=[
                            dcc.Input(
                                id="rf--feature-name",
                                type="text",
                                placeholder="Enter feature name",
                                required=True,
                            ),
                        ],
                    )
                ),
            ),
            html.Div(
                children=[
                    html.H3("Enter your BDD Scenarios"),
                    html.H4(
                        "Add the BDD tags before each Scenario keyword to track the test level/approach for coverage purposes."
                    ),
                    html.H4(
                        f"""Test Levels: 
                            @{Constants.TestLevelsEntity.INTEGRATION}
                            @{Constants.TestLevelsEntity.COMPONENT}
                            @{Constants.TestLevelsEntity.CONTRACT}
                            @{Constants.TestLevelsEntity.API}
                            @{Constants.TestLevelsEntity.E2E}
                            @{Constants.TestLevelsEntity.PERFORMANCE}
                            @{Constants.TestLevelsEntity.SECURITY}
                            @{Constants.TestLevelsEntity.USABILITY}
                            @{Constants.TestLevelsEntity.EXPLORATORY}
                        """,
                        className="info-highlight",
                    ),
                    html.H4(
                        f"""Test Approaches: 
                            @{Constants.TestTypesEntity.AUTOMATED}
                            @{Constants.TestTypesEntity.MANUAL}
                        """,
                        className="info-highlight",
                    ),
                    dcc.Textarea(
                        id="rf--bdd-editor",
                        style={"height": "400px"},
                        value="""# Example
Feature: User Login

@automated @e2e
Scenario: Successful login
    Given the user is on the login page
    When they enter valid credentials
    Then they should be redirected to the dashboard
""",
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            html.Div(
                id="rf--bdd-output-message",
                className="output-msg",
            ),
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                "Save feature",
                                id="rf--submit-bdd-button",
                                n_clicks=0,
                                className="submit-btn",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                "Delete File",
                                id="rf--delete-bdd-file-button",
                                n_clicks=0,
                            ),
                        ]
                    ),
                ],
            ),
        ],
        style={"display": "block"},
    )


def register_scripted_test_cases():
    return html.Div(
        id="rf--scripted-container",
        className="section-group",
        children=[
            dcc.Input(
                id="rf--test-name",
                type="text",
                placeholder="Enter test case title",
                required=True,
            ),
            dcc.Dropdown(
                options=TestEffortsMapper.get_list_of_test_levels(),
                id="rf--test-level",
                placeholder="Enter test level",
                searchable=True,
                className="c_dropdown",
                value="exploratory",
            ),
            dcc.RadioItems(
                id="rf--test-approach",
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
            html.H3("Enter the Preconditions for this Test Case:"),
            html.Div(
                id="rf--preconditions-container",
                children=[
                    dcc.Textarea(
                        id="rf--precondition-1",
                        placeholder="Enter precondition 1",
                        required=True,
                    )
                ],
            ),
            html.Button(
                "+ Add Precondition",
                id="rf--add-precondition",
                n_clicks=0,
                className="add-precondition-btn",
            ),
            html.H3("Enter the Test Case steps and expected results:"),
            html.Div(
                id="rf--steps-container",
                className="grid grid-2",
                children=[
                    dcc.Textarea(
                        id="rf--step-1",
                        placeholder="Enter step 1",
                        required=True,
                    ),
                    dcc.Textarea(
                        id="rf--expected-1",
                        placeholder="Enter expected result 1",
                        required=True,
                    ),
                ],
            ),
            html.Button(
                "+ Add Step",
                id="rf--add-step",
                n_clicks=0,
                className="add-step-btn",
            ),
            html.Div(
                id="rf--scripted-output-message",
                className="output-msg",
            ),
            html.Div(
                className="grid grid-2",
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                "Save new test",
                                id="rf--submit-scripted-button",
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
