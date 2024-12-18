import dash
from dash.dependencies import Input, Output

import src.views.layout.html_dashboard as html_dashboard
from src.utils.constants.constants import Constants


data_path = Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH
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
            slice_values=Constants.TestEffortsDataJSON.TOTAL_TIME,
            names=Constants.TestEffortsDataJSON.TEST_NAME,
            title="Test Effort Distribution",
        ),
        bar_fig.create(
            x_axis=Constants.TestEffortsDataJSON.TEST_LEVEL,
            y_axis=Constants.TestEffortsDataJSON.TEST_APPROACH,
            title="Test Pyramid",
        ),
        line_fig.create(
            x_axis=Constants.TestEffortsDataJSON.TEST_NAME,
            y_axis=Constants.TestEffortsDataJSON.TOTAL_TIME,
            title="Total Time of Manual testing",
        ),
    )


app.layout = html_dashboard.render_layout()
