import base64
import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output

from src.models.entity.chart.pie_chart import PieChart
from src.models.entity.chart.bar_chart import BarChart
from src.models.entity.chart.line_chart import LineChart
from src.models.entity.chart.pyramid_chart import PyramidChart

from src.models.mapper.data_mapper import DataMapper
from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


data_path = Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH
data_mapper_instance = DataMapper(filename=data_path)


def update_figures():
    chart_args_test_names_and_times = [
        ("data_frame", TestEffortsMapper.filter_test_names_and_times_dictionary()),
        ("template", "plotly_dark"),
    ]

    line_fig = LineChart(**dict(chart_args_test_names_and_times))

    return line_fig


def render_layout():
    line_fig = update_figures()

    plot_line_chart_effort = dcc.Graph(
        id="line-chart",
        figure=line_fig.create(
            x_axis=Constants.ScenariosDataJSON.TEST_NAME,
            y_axis=Constants.ScenariosDataJSON.TOTAL_TIME,
            title="Test Effort Distribution (in seconds)",
        ),
    )

    dashboard_layout = html.Div(
        [
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.DASHBOARD
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.DASHBOARD
            ),
            dcc.Dropdown(
                id="dash--project-dropdown",
                placeholder=Constants.FieldText.SELECT_PROJECT_NAME,
                options=ProjectMapper.get_project_options(),
                className="c_dropdown required",
            ),
            html.Div(
                className="content-frame",
                children=[
                    html.H2(
                        children="Test Coverage, Distribution & Execution Effort",
                        className="header-card",
                    ),
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                id="dash--pie-chart-test-approaches",
                                className="chart-card-flex",
                            ),
                            html.Div(
                                id="dash--pie-chart-suite-test-balance",
                                className="chart-card-flex",
                            ),
                        ],
                    ),
                    html.Div(
                        id="dash--test-pyramid-chart",
                        className="chart-card",
                    ),
                    html.Div(
                        children=plot_line_chart_effort,
                        id="line-chart-container",
                        className="chart-card",
                    ),
                ],
            ),
        ]
    )

    return dashboard_layout
