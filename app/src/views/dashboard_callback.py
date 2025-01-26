import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output
from src.models.entity.chart.pyramid_chart import PyramidChart
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
            title=Constants.FieldText.CHART_TEST_EFFORT_DISTRIBUTION,
        ),
        bar_fig.create(
            x_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            y_axis=Constants.ScenariosDataJSON.TEST_APPROACH,
            title=Constants.FieldText.CHART_TEST_PYRAMID,
        ),
        line_fig.create(
            x_axis=Constants.ScenariosDataJSON.TEST_NAME,
            y_axis=Constants.ScenariosDataJSON.TOTAL_TIME,
            title=Constants.FieldText.CHART_TOTAL_TIME_OF_MANUAL_TESTING,
        ),
    )


@callback(
    Output("dash--pie-chart-test-approaches", "children"),
    Input("dash--project-dropdown", "value"),
)
def update_test_approaches_pie_chart(selected_project_id):
    if not selected_project_id:
        return render_message_for_unselected_project()

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
    automated_result_as_green = "seagreen"
    manual_result_as_orange = "orange"

    return dcc.Graph(
        id="pie-chart",
        figure=pie_fig.create(
            slice_values=Constants.ScenariosDataJSON.COUNT,
            names=Constants.ScenariosDataJSON.TEST_APPROACH,
            title=Constants.FieldText.TEST_COVERAGE_AUTOMATED_VS_MANUAL,
            slice_colors=[manual_result_as_orange, automated_result_as_green],
        ),
    )


@callback(
    Output("dash--pie-chart-suite-test-balance", "children"),
    Input("dash--project-dropdown", "value"),
)
def update_tests_per_suite_pie_chart(selected_project_id):
    if not selected_project_id:
        return render_message_for_unselected_project()

    summed_data = TestEffortsMapper.filter_test_suites_by_project(selected_project_id)
    there_is_no_data_selected = not summed_data or all(
        entry[Constants.FeaturesDataJSON.QTY_OF_SCENARIOS] == 0 for entry in summed_data
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
            slice_values=Constants.FeaturesDataJSON.QTY_OF_SCENARIOS,
            names=Constants.SuiteDataJSON.SUITE_NAME,
            title=Constants.FieldText.BALANCE_OF_TESTS_PER_SUITE,
            slice_colors=["seagreen", "orange"],
        ),
    )


@callback(
    Output("dash--test-pyramid-chart", "children"),
    Input("dash--project-dropdown", "value"),
)
def update_test_pyramid_chart(selected_project_id):
    if not selected_project_id:
        return render_message_for_unselected_project()

    summed_data = TestEffortsMapper.filter_counted_test_level_and_approaches_by_project(
        selected_project_id
    )
    there_is_no_data_selected = not summed_data or all(
        entry[Constants.ScenariosDataJSON.COUNT] == 0 for entry in summed_data
    )

    if there_is_no_data_selected:
        return html.Div(
            Constants.Messages.NO_DATA_AVAILABLE_FOR_THE_SELECTED_PROJECT,
            style={"textAlign": "center", "color": "grey"},
        )

    chart_args_test_segregated_levels_and_approaches = [
        (
            "data_frame_group_a",
            TestEffortsMapper.filter_test_level_and_approaches_by_project(
                selected_project_id,
                data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH,
                filter_by_key=Constants.ScenariosDataJSON.TEST_APPROACH,
                filter_by_value=Constants.TestTypesEntity.AUTOMATED,
            ),
        ),
        (
            "data_frame_group_b",
            TestEffortsMapper.filter_test_level_and_approaches_by_project(
                selected_project_id,
                data_path=Constants.FilePaths.SCENARIOS_DATA_JSON_PATH,
                filter_by_key=Constants.ScenariosDataJSON.TEST_APPROACH,
                filter_by_value=Constants.TestTypesEntity.MANUAL,
            ),
        ),
        ("template", "plotly_dark"),
    ]

    pyramid_fig = PyramidChart(**dict(chart_args_test_segregated_levels_and_approaches))

    return dcc.Graph(
        id="pyramid-chart",
        figure=pyramid_fig.create(
            x_group_a_axis=Constants.ScenariosDataJSON.COUNT,
            y_group_a_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            x_group_b_axis=Constants.ScenariosDataJSON.COUNT,
            y_group_b_axis=Constants.ScenariosDataJSON.TEST_LEVEL,
            title_x="Total tests",
            title_y="Test level",
            legend_group_a_axis="Automated",
            legend_group_b_axis="Manual",
            title="Test Pyramid - Coverage per level & approach",
        ),
    )


def render_message_for_unselected_project():
    return html.Div(
        Constants.FieldText.PLEASE_SELECT_A_PROJECT_TO_VIEW_CHART,
        style={"textAlign": "center", "color": "red"},
    )


def is_the_project_selected(project_id):
    if not project_id:
        return html.Div(
            Constants.FieldText.PLEASE_SELECT_A_PROJECT_TO_VIEW_CHART,
            style={"textAlign": "center", "color": "red"},
        )


app.layout = html_dashboard.render_layout()
