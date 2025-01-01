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
                                                placeholder=Constants.FieldText.PROJECT_ID,
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid",
                                            ),
                                            html.Button(
                                                Constants.FieldText.GENERATE_NEW_ID,
                                                id="rpj--generate-id-button",
                                                className="inline-grid",
                                            ),
                                        ],
                                    ),
                                    dcc.Input(
                                        id="rpj--project-name",
                                        type="text",
                                        placeholder=Constants.FieldText.ENTER_PROJECT_NAME,
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label(
                        Constants.FieldText.REQUIRED_FIELDS, className="required-msg"
                    ),
                    html.Div(id="rpj--output-message-projects", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button(
                                Constants.FieldText.SAVE,
                                id="rpj--save-button",
                                n_clicks=0,
                            ),
                            html.Button(
                                Constants.FieldText.UPDATE,
                                id="rpj--update-button",
                                n_clicks=0,
                            ),
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
                                        placeholder=Constants.FieldText.ENTER_PROJECT_ID_TO_DELETE,
                                    ),
                                    html.Button(
                                        Constants.FieldText.DELETE,
                                        id="rpj--delete-button",
                                        n_clicks=0,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
