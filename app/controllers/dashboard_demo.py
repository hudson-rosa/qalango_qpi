import dash
import dash_core_components as dcc
import dash_html_components as html

import os, sys

# Get the path to the directory containing the 'app' package
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the directory containing the 'app' package to the Python path
sys.path.append(app_dir)

from app.utils.data_handler import DataHandler
from app.models.entity.pie_chart import PieChart
from app.models.entity.bar_chart import BarChart
from app.models.entity.line_chart import LineChart


external_stylesheets = ["./assets/static/dashboard_stylesheet.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

chart_args_entries = [
    ("data_frame", DataHandler().compose_data_frame()),
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

app.layout = html.Div(
    [
        html.Div(
            className="content-frame",
            children=[
                html.H1(
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

"""
    Access the dashboard via http://127.0.0.1:8050/
"""
if __name__ == "__main__":
    app.run(debug=True)
