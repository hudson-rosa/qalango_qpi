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
                            html.Div(
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
                            ),
                            html.Div(
                                className="grid grid-2",
                                children=[
                                    dcc.Dropdown(
                                        id="rf--project-name",
                                        options=ProjectMapper.get_project_options(),
                                        placeholder="Select project name",
                                        searchable=True,
                                        className="c_dropdown",
                                    ),
                                    dcc.Dropdown(
                                        id="rf--suite-name",
                                        options=SuiteMapper.get_suite_options(),
                                        placeholder="Select suite name",
                                        searchable=True,
                                        className="c_dropdown",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Container for BDD Scenarios registration
                    html.Div(
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
                                    html.H3("Enter your BDD Scenarios:"),
                                    dcc.Textarea(
                                        id="rf--bdd-editor",
                                        style={"height": "400px"},
                                        value="""# Example - BDD scenario
    Feature: User Login

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
                    ),
                    # Container for Scripted Test registration
                    html.Div(
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
                    ),
                ],
            ),
        ]
    )
