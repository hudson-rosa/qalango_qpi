from dash import dcc, html
from src.utils.assets_handler import AssetsHandler
from src.models.entity.test_level import TestLevel
from src.models.mapper.project_mapper import ProjectMapper
import src.controllers.app_path_config as app_path_config


decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def generate_marks():
    marks = {}
    step_size = 15
    num_intervals = 30

    # First 5 minutes: steps of 1 minute
    for i in range(0, 6, 1):
        marks[i] = f"{i%60:01d}"

    # Subsequent 15 minutes: steps of 3 minutes
    for i in range(6, 16, 3):
        marks[i] = f"{i%60:01d}"

    # Subsequent minutes until 3 hours: steps of 15 minutes
    for i in range(num_intervals + 1):
        time_in_minutes = i * step_size
        hours = time_in_minutes // 60
        minutes = time_in_minutes % 60
        marks[time_in_minutes] = f"{hours}:{minutes:02d}"

    return marks


slider_marks = generate_marks()

select_project = ProjectMapper.get_project_options()


def render_layout():
    return html.Div(
        [
            html.Img(
                src=decoded_logo_img,
                className="qpi_logo",
            ),
            html.H1("Testing Efforts"),
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
                        className="tab--selected",
                    ),
                    dcc.Link(
                        "Register Project",
                        href="/register_project",
                        className="tab--unselected",
                    ),
                ],
            ),
            html.Div(
                className="content-frame",
                children=[
                    html.Div(
                        children="Enter the test details to ensure realistic KPIs for Quality Assurance",
                        className="header-card",
                    )
                ],
            ),
            html.Div(
                className="form-content",
                children=[
                    html.Ul(
                        html.Li(
                            html.Div(
                                className="grid grid-2",
                                children=[
                                    dcc.Input(
                                        id="rte--test-name",
                                        type="text",
                                        placeholder="Enter test title",
                                        required=True,
                                    ),
                                    dcc.Input(
                                        id="rte--test-suite",
                                        type="text",
                                        placeholder="Enter test suite",
                                        required=True,
                                    ),
                                    dcc.Dropdown(
                                        id="rte--project-name",
                                        options=select_project,
                                        placeholder="Select project name",
                                        searchable=True,
                                        className="c_dropdown",
                                    ),
                                    dcc.Dropdown(
                                        options=[
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "unit"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "unit"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "integration"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "integration"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "component"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "component"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "contract"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "contract"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "api"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "api"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "e2e"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "e2e"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "performance"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "performance"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "security"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "security"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "usability"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "usability"
                                                ),
                                            },
                                            {
                                                "label": TestLevel().get_option(
                                                    "label", "exploratory"
                                                ),
                                                "value": TestLevel().get_option(
                                                    "ref", "exploratory"
                                                ),
                                            },
                                        ],
                                        id="rte--test-level",
                                        placeholder="Enter test level",
                                        searchable=True,
                                        className="c_dropdown",
                                        value="exploratory",
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Enter total test execution time"),
                                            dcc.Slider(
                                                id="rte--total-time",
                                                min=0,
                                                max=301,
                                                marks=slider_marks,
                                                step=None,
                                                value=0,
                                                included=False,
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True,
                                                },
                                                className="c_slider",
                                            ),
                                            html.H5(id="rte--slider-output"),
                                        ]
                                    ),
                                    dcc.RadioItems(
                                        id="rte--test-approach",
                                        options=[
                                            {"label": "Manual", "value": "manual"},
                                            {
                                                "label": "Automated",
                                                "value": "automated",
                                            },
                                        ],
                                        className="c_radio",
                                        value="manual",
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label("Required fields", className="required-msg"),
                    html.Div(id="rte--output-message", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button("Save", id="rte--save-button", n_clicks=0),
                            html.Button("Update", id="rte--update-button", n_clicks=0),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rte--delete-output-message",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rte--delete-test-name",
                                        type="text",
                                        placeholder="Enter an existing Test Title to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="rte--delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
