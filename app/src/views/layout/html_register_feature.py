from dash import dcc, html

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
                    html.Ul(
                        html.Li(
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            dcc.Input(
                                                id="rf--feature-id",
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
                                    dcc.Input(
                                        id="rf--feature-name",
                                        type="text",
                                        placeholder="Enter feature name",
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Div(
                        children=[
                            html.H3("Enter your BDD Scenarios:"),
                            dcc.Textarea(
                                id="rf--bdd-editor",
                                style={"width": "100%", "height": "300px"},
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
                        id="rf--output-message",
                        className="output-msg",
                    ),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Div(
                                children=[
                                    html.Button(
                                        "Submit Feature",
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
                                        id="rf--delete-file-button",
                                        n_clicks=0,
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
