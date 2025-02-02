from dash import dcc, html

from src.models.mapper.data_mapper import DataMapper
from src.models.mapper.project_mapper import ProjectMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants


data_path = Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH
data_mapper_instance = DataMapper(filename=data_path)


def render_layout():

    dashboard_layout = html.Div(
        [
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.DASHBOARD
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.DASHBOARD
            ),
            dcc.Dropdown(
                id="dash--project-dropdown",
                placeholder=Constants.FieldText.SELECT_PROJECT_NAME,
                options=ProjectMapper.get_project_options(),
                className="c_dropdown required",
            ),
            html.Div(
                className="content-frame",
                children=[
                    html.H2(
                        children="Test Coverage, Distribution & Execution Effort",
                        className="header-card",
                    ),
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                id="dash--pie-chart-test-approaches",
                                className="chart-card-flex",
                            ),
                            html.Div(
                                id="dash--pie-chart-suite-test-balance",
                                className="chart-card-flex",
                            ),
                        ],
                    ),
                    html.Div(
                        id="dash--test-pyramid-chart",
                        className="chart-card",
                    ),
                    html.Div(
                        id="dash--tine-chart-tests-duration",
                        className="chart-card",
                    ),
                ],
            ),
        ]
    )

    return dashboard_layout
