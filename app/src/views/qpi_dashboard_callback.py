import dash
from dash.dependencies import Input, Output

import src.views.layout.html_dashboard as html_dashboard
import src.controllers.app_path_config as app_path_config

data_path = app_path_config.get_data_storage_path()
app = dash.Dash(__name__)


@app.callback(
    [
        Output("pie-chart", "figure"),
        Output("bar-chart", "figure"),
        Output("line-chart", "figure"),
    ]
)
def refresh_charts():

    pie_fig, bar_fig, line_fig = html_dashboard.update_figures()

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


app.layout = html_dashboard.render_layout()
