import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output
from src.models.entity.chart.pie_chart import PieChart

from src.models.mapper.test_efforts_mapper import TestEffortsMapper
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
            slice_values=Constants.ScenariosDataJSON.TOTAL_TIME,
            names=Constants.ScenariosDataJSON.TEST_NAME,
            title="Test Effort Distribution",
        ),
        bar_fig.create(
            x_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            y_axis=Constants.ScenariosDataJSON.TEST_APPROACH,
            title="Test Pyramid",
        ),
        line_fig.create(
            x_axis=Constants.ScenariosDataJSON.TEST_NAME,
            y_axis=Constants.ScenariosDataJSON.TOTAL_TIME,
            title="Total Time of Manual testing",
        ),
    )


@callback(
    Output("dash--pie-chart-test-approaches", "children"),
    Input("dash--project-dropdown", "value"),
)
def update_test_approaches_pie_chart(selected_project_id):
    if not selected_project_id:
        return html.Div(
            "Please select a project to view the chart.",
            style={"textAlign": "center", "color": "red"},
        )

    summed_data = TestEffortsMapper.sum_test_approaches_by_project(selected_project_id)
    there_is_no_data_selected = not summed_data or all(
        entry[Constants.ScenariosDataJSON.COUNT] == 0 for entry in summed_data
    )

    if there_is_no_data_selected:
        return html.Div(
            Constants.Messages.NO_DATA_AVAILABLE_FOR_THE_SELECTED_PROJECT,
            style={"textAlign": "center", "color": "grey"},
        )

    pie_fig = PieChart(data_frame=summed_data, template="plotly_dark")

    return dcc.Graph(
        id="pie-chart",
        figure=pie_fig.create(
            slice_values=Constants.ScenariosDataJSON.COUNT,
            names=Constants.ScenariosDataJSON.TEST_APPROACH,
            title=Constants.FieldText.TEST_COVERAGE_AUTOMATED_VS_MANUAL,
            slice_colors=["seagreen", "orange"],
        ),
    )


app.layout = html_dashboard.render_layout()
