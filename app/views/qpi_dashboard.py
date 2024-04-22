import dash
from dash import dcc, html

from app.utils.json_data_handler import JsonDataHandler
from app.models.entity.pie_chart import PieChart
from app.models.entity.bar_chart import BarChart
from app.models.entity.line_chart import LineChart

app = dash.Dash(__name__)

chart_args_entries = [
    ("data_frame", JsonDataHandler().compose_data_frame()),
    ("template", "plotly_dark"),
]
pie_fig = PieChart(**dict(chart_args_entries))
bar_fig = BarChart(**dict(chart_args_entries))
line_fig = LineChart(**dict(chart_args_entries))

plot_pie_chart = dcc.Graph(
    id="pie-chart",
    figure=pie_fig.create(
        slice_values="score", names="test_name", title="Scores Distribution"
    ),
)

plot_bar_chart = dcc.Graph(
    id="bar-chart",
    figure=bar_fig.create(
        x_axis="test_name",
        y_axis="score",
        title="Scores Distribution",
    ),
)

plot_line_chart = dcc.Graph(
    id="line-chart",
    figure=line_fig.create(
        x_axis="test_date",
        y_axis="score",
        title="Scores Over Time",
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
                    className="chart-card",
                ),
                html.Div(
                    children=plot_bar_chart,
                    className="chart-card",
                ),
                html.Div(
                    children=plot_line_chart,
                    className="chart-card",
                ),
            ],
        ),
    ]
)

app.layout = dashboard_layout
