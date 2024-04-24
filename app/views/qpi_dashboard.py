import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output

from app.utils.json_data_handler import JsonDataHandler
from app.models.entity.pie_chart import PieChart
from app.models.entity.bar_chart import BarChart
from app.models.entity.line_chart import LineChart

from app.models.data_processing import DataProcessing
import app.controllers.app_path_config as app_path_config

data_path = app_path_config.get_data_storage_path()
app = dash.Dash(__name__)


def update_figures():
    chart_args_entries = [
        ("data_frame", DataProcessing.get_test_names_and_times_dictionary()),
        ("template", "plotly_dark"),
    ]

    pie_fig = PieChart(**dict(chart_args_entries))
    bar_fig = BarChart(**dict(chart_args_entries))
    line_fig = LineChart(**dict(chart_args_entries))

    print("\n------->>> RAW DATA: \n", JsonDataHandler(data_path).compose_data_frame())
    print("\n------->>> PROCESSED DATA: \n", chart_args_entries)
    return pie_fig, bar_fig, line_fig

pie_fig, bar_fig, line_fig = update_figures()

plot_pie_chart = dcc.Graph(
    id="pie-chart",
    figure=pie_fig.create(
        slice_values="total_time", names="test_name", title="Test Effort Distribution"
    ),
)

plot_bar_chart = dcc.Graph(
    id="bar-chart",
    figure=bar_fig.create(
        x_axis="test_name",
        y_axis="total_time",
        title="Tests Distribution",
    ),
)

plot_line_chart = dcc.Graph(
    id="line-chart",
    figure=line_fig.create(
        x_axis="test_name",
        y_axis="total_time",
        title="Total Time of Manual testing",
    ),
)

dashboard_layout = html.Div(
    [
        html.H1("Dashboard Page"),
        dcc.Link("Go to Testing Efforts Registration", href="/register_tests"),
        html.Div(
            className="content-frame",
            children=[
                html.H2(
                    children="Test Scores Dashboard",
                    className="header-card",
                ),
                html.Div(
                    children="A modern and interactive dashboard for test scores visualization.",
                    className="header-card",
                ),
                html.Div(
                    children=plot_pie_chart,
                    id="pie-chart-container",
                    className="chart-card",
                ),
                html.Div(
                    children=plot_bar_chart,
                    id="bar-chart-container",
                    className="chart-card",
                ),
                html.Div(
                    children=plot_line_chart,
                    id="line-chart-container",
                    className="chart-card",
                ),
            ],
        ),
    ]
)

app.layout = dashboard_layout
