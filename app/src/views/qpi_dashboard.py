import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output

from ..utils.json_data_handler import JsonDataHandler
from ..models.entity.pie_chart import PieChart
from ..models.entity.bar_chart import BarChart
from ..models.entity.line_chart import LineChart

from ..models.data_processing import DataProcessing
import src.controllers.app_path_config as app_path_config

data_path = app_path_config.get_data_storage_path()
app = dash.Dash(__name__)


def update_figures():
    chart_args_test_names_and_times = [
        ("data_frame", DataProcessing.get_test_names_and_times_dictionary()),
        ("template", "plotly_dark"),
    ]
    chart_args_test_categories_and_approaches = [
        ("data_frame", DataProcessing.get_test_category_and_approaches()),
        ("template", "plotly_dark"),
    ]

    pie_fig = PieChart(**dict(chart_args_test_names_and_times))
    bar_fig = BarChart(**dict(chart_args_test_categories_and_approaches))
    line_fig = LineChart(**dict(chart_args_test_names_and_times))

    print("\n------->>> RAW DATA: \n", JsonDataHandler(data_path).compose_data_frame())
    print("\n------->>> PROCESSED DATA - TEST NAMES / TIMES: \n", chart_args_test_names_and_times)
    print("\n------->>> PROCESSED DATA - TEST CATEGORIES / APPROACHES: \n", chart_args_test_categories_and_approaches)
    return pie_fig, bar_fig, line_fig


@app.callback(
    [
        Output("pie-chart", "figure"),
        Output("bar-chart", "figure"),
        Output("line-chart", "figure"),
    ]
)
def refresh_charts():

    pie_fig, bar_fig, line_fig = update_figures()

    print("Figures updated")
    return (
        pie_fig.create(
            slice_values="total_time",
            names="test_name",
            title="Test Effort Distribution",
        ),
        bar_fig.create(
            x_axis="test_category",
            y_axis="test_approach",
            title="Test Pyramid",
        ),
        line_fig.create(
            x_axis="test_name",
            y_axis="total_time",
            title="Total Time of Manual testing",
        ),
    )


def render_layout():
    pie_fig, bar_fig, line_fig = update_figures()

    plot_pie_chart = dcc.Graph(
        id="pie-chart",
        figure=pie_fig.create(
            slice_values="total_time",
            names="test_name",
            title="Test Effort Distribution",
        ),
    )

    plot_bar_chart = dcc.Graph(
        id="bar-chart",
        figure=bar_fig.create(
            x_axis="test_category",
            y_axis="count",
            title="Test Pyramid",
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
                        children="Test Efforts Dashboard",
                        className="header-card",
                    ),
                    html.Div(
                        children="Check here all the details regarding the manual testing efforts",
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

    return dashboard_layout


app.layout = render_layout
