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
                                                id="rsu--suite-id",
                                                type="text",
                                                placeholder=Constants.FieldText.SUITE_ID,
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid",
                                            ),
                                            html.Button(
                                                Constants.FieldText.GENERATE_NEW_ID,
                                                id="rsu--generate-id-button",
                                                className="inline-grid",
                                            ),
                                        ],
                                    ),
                                    dcc.Dropdown(
                                        id="rsu--project-dropdown",
                                        placeholder=Constants.FieldText.SELECT_PROJECT_NAME,
                                        options=ProjectMapper.get_project_options(),
                                        className=" c_dropdown required",
                                    ),
                                    dcc.Input(
                                        id="rsu--suite-name",
                                        type="text",
                                        placeholder=Constants.FieldText.ENTER_SUITE_NAME,
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label(
                        Constants.FieldText.REQUIRED_FIELDS, className="required-msg"
                    ),
                    html.Div(id="rsu--output-message-suites", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button(
                                Constants.FieldText.SAVE,
                                id="rsu--save-button",
                                n_clicks=0,
                            ),
                            html.Button(
                                Constants.FieldText.UPDATE,
                                id="rsu--update-button",
                                n_clicks=0,
                            ),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rsu--delete-output-message-suites",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rsu--delete-suite-id",
                                        type="text",
                                        placeholder=Constants.FieldText.ENTER_SUITE_ID_TO_DELETE,
                                    ),
                                    html.Button(
                                        Constants.FieldText.DELETE,
                                        id="rsu--delete-button",
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
