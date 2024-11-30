import random
import string
from dash import dcc, html
from src.utils.assets_handler import AssetsHandler
from src.models.entity.test_level import TestLevel
import src.controllers.app_path_config as app_path_config


decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def render_layout():
    return html.Div(
        [
            html.Img(
                src=decoded_logo_img,
                className="qpi_logo",
            ),
            html.H1("Project"),
            html.Div(
                className="tabs",
                children=[
                    dcc.Link(
                        "View Analytics Dashboard",
                        href="/dashboard",
                        className="tab--unselected",
                    ),
                    dcc.Link(
                        "Register Test Efforts",
                        href="/register_tests",
                        className="tab--unselected",
                    ),
                    dcc.Link(
                        "Register Project",
                        href="/register_project",
                        className="tab--selected",
                    ),
                ],
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
                                                id="rp--project-id",
                                                type="text",
                                                placeholder="Project id",
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid"
                                            ),
                                            html.Button(
                                                "Generate new ID",
                                                id="rp--generate-id-button",
                                                className="inline-grid"
                                            ),
                                        ],
                                    ),
                                    dcc.Input(
                                        id="rp--project-name",
                                        type="text",
                                        placeholder="Enter project name",
                                        required=True
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label("Required fields", className="required-msg"),
                    html.Div(id="rp--output-message", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button("Save", id="rp--save-button", n_clicks=0),
                            html.Button("Update", id="rp--update-button", n_clicks=0),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rp--delete-output-message",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rp--delete-project-id",
                                        type="text",
                                        placeholder="Enter a project ID to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="rp--delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
