from dash import dcc, html

from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


def generate_slider_marks():
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


slider_marks = generate_slider_marks()

select_project = ProjectMapper.get_project_options()


def render_layout():
    return html.Div(
        [
            html_component_header_tabs.render_logo(),
            html_component_header_tabs.render_page_title(
                current_page_identifier=Constants.PageIdentifiers.TEST_EFFORTS
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.TEST_EFFORTS
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
                                        options=TestEffortsMapper.get_list_of_test_levels(),
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
