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

    chart_args_test_segregated_levels_and_approaches = [
        (
            "data_frame_group_a",
            TestEffortsMapper.filter_test_level_and_approaches_by(
                filter_by_key=Constants.ScenariosDataJSON.TEST_APPROACH,
                filter_by_value=Constants.TestTypesEntity.AUTOMATED,
            ),
        ),
        (
            "data_frame_group_b",
            TestEffortsMapper.filter_test_level_and_approaches_by(
                filter_by_key=Constants.ScenariosDataJSON.TEST_APPROACH,
                filter_by_value=Constants.TestTypesEntity.MANUAL,
            ),
        ),
        ("template", "plotly_dark"),
    ]

    line_fig = LineChart(**dict(chart_args_test_names_and_times))
    pyramid_fig = PyramidChart(**dict(chart_args_test_segregated_levels_and_approaches))

    return line_fig, pyramid_fig


def render_layout():
    line_fig, pyramid_fig = update_figures()

    plot_pyramid_chart = dcc.Graph(
        id="pyramid-chart",
        figure=pyramid_fig.create(
            x_group_a_axis="count",
            y_group_a_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            x_group_b_axis="count",
            y_group_b_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            title_x="Total tests",
            title_y="Test level",
            legend_group_a_axis="Automated",
            legend_group_b_axis="Manual",
            title="Test Pyramid Coverage (per level)",
        ),
    )

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
                        children=plot_pyramid_chart,
                        id="pyramid-chart-container",
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
