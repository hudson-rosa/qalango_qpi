import base64
import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output

from src.utils.assets_handler import AssetsHandler
from src.utils.json_data_handler import JsonDataHandler
from src.models.entity.pie_chart import PieChart
from src.models.entity.bar_chart import BarChart
from src.models.entity.line_chart import LineChart
from src.models.entity.pyramid_chart import PyramidChart

from src.models.data_processing import DataProcessing
import src.controllers.app_path_config as app_path_config


data_path = app_path_config.get_data_storage_path()
decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def update_figures():
    chart_args_test_names_and_times = [
        ("data_frame", DataProcessing.filter_test_names_and_times_dictionary()),
        ("template", "plotly_dark"),
    ]
    chart_args_test_categories_and_approaches = [
        ("data_frame", DataProcessing.filter_test_category_and_approaches()),
        ("template", "plotly_dark"),
    ]
    chart_args_test_suites = [
        ("data_frame", DataProcessing.filter_test_suites()),
        ("template", "plotly_dark"),
    ]

    chart_args_test_segregated_categories_and_approaches = [
        (
            "data_frame_group_a",
            DataProcessing.filter_test_category_and_approaches_by(
                filter_by_key="test_approach", filter_by_value="automated"
            ),
        ),
        (
            "data_frame_group_b",
            DataProcessing.filter_test_category_and_approaches_by(
                filter_by_key="test_approach", filter_by_value="manual"
            ),
        ),
        ("template", "plotly_dark"),
    ]

    pie_fig_1 = PieChart(**dict(chart_args_test_categories_and_approaches))
    pie_fig_2 = PieChart(**dict(chart_args_test_suites))
    bar_fig_1 = BarChart(**dict(chart_args_test_names_and_times))
    line_fig = LineChart(**dict(chart_args_test_names_and_times))
    pyramid_fig = PyramidChart(
        **dict(chart_args_test_segregated_categories_and_approaches)
    )
    bar_fig_2 = BarChart(**dict(chart_args_test_suites))

    print("\n------->>> RAW DATA: \n", JsonDataHandler(data_path).compose_data_frame())

    return pie_fig_1, pie_fig_2, bar_fig_1, bar_fig_2, line_fig, pyramid_fig


def render_layout():
    pie_fig_1, pie_fig_2, bar_fig_1, bar_fig_2, line_fig, pyramid_fig = update_figures()

    plot_pie_chart_1 = dcc.Graph(
        id="pie-chart",
        figure=pie_fig_1.create(
            slice_values="count",
            names="test_approach",
            title="Test Coverage: Automated Vs. Manual",
            slice_colors=["seagreen", "orange"],
        ),
    )

    plot_pie_chart_2 = dcc.Graph(
        id="pie-chart",
        figure=pie_fig_2.create(
            slice_values="count", names="test_suites", title="Test Coverage per Suite"
        ),
    )

    plot_pyramid_chart = dcc.Graph(
        id="pyramid-chart",
        figure=pyramid_fig.create(
            x_group_a_axis="count",
            y_group_a_axis="test_category",
            x_group_b_axis="count",
            y_group_b_axis="test_category",
            title_x="Total tests",
            title_y="Test category",
            legend_group_a_axis="Automated",
            legend_group_b_axis="Manual",
            title="Test Pyramid Coverage",
        ),
    )

    plot_bar_chart = dcc.Graph(
        id="bar-chart",
        figure=bar_fig_1.create(
            x_axis="test_name", y_axis="total_time", title="Test Effort Distribution"
        ),
    )

    plot_line_chart = dcc.Graph(
        id="line-chart",
        figure=line_fig.create(
            x_axis="test_name",
            y_axis="total_time",
            title="Test Effort Distribution",
        ),
    )

    plot_bar_chart_2 = dcc.Graph(
        id="line-chart",
        figure=bar_fig_2.create(
            x_axis="test_suites",
            y_axis="count",
            title="Total Tests per Suite",
        ),
    )

    dashboard_layout = html.Div(
        [
            html.Img(
                src=decoded_logo_img,
                className="qpi_logo",
            ),
            html.H1("Analytics"),
            html.Div(
                className="tabs",
                children=[
                    dcc.Link(
                        "Register Test Efforts",
                        href="/register_tests",
                        className="tab--unselected",
                    ),
                    dcc.Link(
                        "View Analytics Dashboard",
                        href="/dashboard",
                        className="tab--selected",
                    ),
                ],
            ),
            html.Div(
                className="content-frame",
                children=[
                    html.H2(
                        children="Test Efforts Dashboard",
                        className="header-card",
                    ),
                    html.Div(
                        children="Check here all the details regarding the manual testing efforts",
                        className="header-card",
                    ),
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                children=plot_pie_chart_1,
                                id="pie-chart-container",
                                className="chart-card-flex",
                            ),
                            html.Div(
                                children=plot_pie_chart_2,
                                id="pie-chart-container",
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
                        children=plot_line_chart,
                        id="line-chart-container",
                        className="chart-card",
                    ),
                    html.Div(
                        children=plot_bar_chart_2,
                        id="bar-chart-container",
                        className="chart-card",
                    ),
                ],
            ),
        ]
    )

    return dashboard_layout
