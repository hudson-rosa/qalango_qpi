import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.scenarios_editor_mapper import EditScenariosMapper

import src.views.layout.html_edit_scenarios as html_edit_scenarios


app = dash.Dash(__name__)


@callback(
    Output("test-table", "data"),
    Input("esc--project-dropdown", "value")
)
def update_table(selected_project):
    return EditScenariosMapper.parse_scenarios_data(selected_project)


app.layout = html_edit_scenarios.render_layout()
