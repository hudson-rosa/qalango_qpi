from dash import dcc, html

from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


def render_layout():
    return html.Div(
        [
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.PROJECTS
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.PROJECTS
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
                                                id="rpj--project-id",
                                                type="text",
                                                placeholder="Project id",
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid",
                                            ),
                                            html.Button(
                                                "Generate new ID",
                                                id="rpj--generate-id-button",
                                                className="inline-grid",
                                            ),
                                        ],
                                    ),
                                    dcc.Input(
                                        id="rpj--project-name",
                                        type="text",
                                        placeholder="Enter project name",
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label("Required fields", className="required-msg"),
                    html.Div(id="rpj--output-message-projects", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button("Save", id="rpj--save-button", n_clicks=0),
                            html.Button("Update", id="rpj--update-button", n_clicks=0),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rpj--delete-output-message-projects",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rpj--delete-project-id",
                                        type="text",
                                        placeholder="Enter a project ID to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="rpj--delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
