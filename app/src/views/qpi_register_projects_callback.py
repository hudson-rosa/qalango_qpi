import dash
import json
import random
import string
from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.controllers.app_path_config as app_path_config
import src.views.layout.html_register_project as html_register_project
import dash_daq as daq

app = dash.Dash(__name__)

json_storage = app_path_config.get_data_storage_project_path()
data_mapper_instance = DataMapper(filename=json_storage)

def generate_random_id(starts_with="p"):
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return str(f"{starts_with}_{random_id}").lower()

@callback(
    Output("rp--project-id", "value"),
    Input("rp--generate-id-button", "n_clicks"),
    prevent_initial_call=False
)
def update_random_id(n_clicks):
        return generate_random_id()

@callback(
    [Output("rp--output-message", "children"), Output("rp--delete-output-message", "children")],
    [
        Input("rp--save-button", "n_clicks"),
        Input("rp--update-button", "n_clicks"),
        Input("rp--delete-button", "n_clicks"),
    ],
    [
        State("rp--project-id", "value"),
        State("rp--project-name", "value"),
        State("rp--delete-project-id", "value")
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    project_id,
    project_name,
    delete_project_id
):

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rp--save-button":
            try:
                data = data_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            new_data = {
                "project_id": project_id,
                "project_name": project_name
            }
            data[project_id] = new_data

            data_mapper_instance.save_to_json_storage(data)

            return "Project saved successfully", None

        case "rp--update-button":
            try:
                data = data_mapper_instance.load_from_json_storage()
            except FileNotFoundError:
                return None, "No data found. Nothing to update."

            if project_id in data:
                data[project_id]["project_name"] = project_name

                data_mapper_instance.save_to_json_storage(data)

                return "Project updated successfully", None
            else:
                return (
                    None,
                    f'Data with project ID "{project_id}" not found in JSON. Nothing to update.',
                )

        case "rp--delete-button":
            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_project_id in data:
                    del data[delete_project_id]

                    data_mapper_instance.save_to_json_storage(data)

                    return (
                        None,
                        f'Project with test name "{delete_project_id} - {project_name}" deleted successfully',
                    )
                else:
                    return (
                        None,
                        f'Project with test name "{delete_project_id}" not found in JSON',
                    )
            except FileNotFoundError:
                return None, "No data found. Nothing to delete."

        case _:
            return "Please choose an action", None


app.layout = html_register_project.render_layout()
