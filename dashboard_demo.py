import dash
import dash_core_components as dcc
import dash_html_components as html
import data.data_handler as dh
from entity.pie_chart import PieChart
from entity.bar_chart import BarChart
from entity.line_chart import LineChart


external_stylesheets = ["./static/stylesheet.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

chart_args_entries = [
    ("data_frame", dh.DataHandler().compose_data_frame()),
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
