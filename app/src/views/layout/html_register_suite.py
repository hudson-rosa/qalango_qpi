from dash import dcc, html

from src.models.mapper.project_mapper import ProjectMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


def render_layout():
    return html.Div(
        [
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.SUITES
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.SUITES
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
                                                id="rs--suite-id",
                                                type="text",
                                                placeholder="Suite id",
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid",
                                            ),
                                            html.Button(
                                                "Generate new ID",
                                                id="rs--generate-id-button",
                                                className="inline-grid",
                                            ),
                                        ],
                                    ),
                                    dcc.Dropdown(
                                        id="rs--project-dropdown",
                                        placeholder="Select project name",
                                        options=ProjectMapper.get_project_options(),
                                        className="c_dropdown"
                                    ),
                                    dcc.Input(
                                        id="rs--suite-name",
                                        type="text",
                                        placeholder="Enter suite name",
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label("Required fields", className="required-msg"),
                    html.Div(id="rs--output-message-suites", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button("Save", id="rs--save-button", n_clicks=0),
                            html.Button("Update", id="rs--update-button", n_clicks=0),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rs--delete-output-message-suites",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rs--delete-suite-id",
                                        type="text",
                                        placeholder="Enter a suite ID to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="rs--delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
