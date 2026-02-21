from dash import dcc, html, dash_table
from dash_ace import DashAceEditor

from src.models.mapper.scenarios_editor_mapper import EditScenariosMapper
from src.models.mapper.project_mapper import ProjectMapper
from src.models.mapper.suite_mapper import SuiteMapper
from src.models.mapper.test_efforts_mapper import TestEffortsMapper
from src.views.layout import html_component_header_tabs
from src.utils.constants.constants import Constants
from src.utils.data_generator import DataGenerator


def render_layout():
    return html.Div(
        [
            html_component_header_tabs.render_header(
                current_page_identifier=Constants.PageIdentifiers.EDIT_SCENARIOS
            ),
            html_component_header_tabs.render_tabs(
                active_tab_identifier=Constants.PageIdentifiers.EDIT_SCENARIOS
            ),
            dcc.Dropdown(
                id="esc--project-dropdown",
                options=ProjectMapper.get_project_options(),
                placeholder=Constants.FieldText.SELECT_PROJECT_NAME,
                searchable=True,
                className="c_dropdown required",
            ),
            dash_table.DataTable(
                id="test-table",
                columns=[
                    {
                        "name": col,
                        "id": col,
                        "editable": col
                        not in ["Suite ID", "Feature ID", "Scenario ID"],
                    }
                    for col in [
                        "Suite ID",
                        "Suite",
                        "Feature ID",
                        "Feature Name",
                        "Requirements Link",
                        "Scenario ID",
                        "Scenario Name",
                        "Test Level",
                        "Test Approach",
                        "Test Categories",
                        "Test Duration",
                    ]
                ],
                editable=True,
                filter_action="native",
                sort_action="native",
                row_deletable=True,
                style_table={"overflowX": "auto"},
            ),
        ]
    )
