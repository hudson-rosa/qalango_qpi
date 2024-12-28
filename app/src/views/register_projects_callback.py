import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_project as html_register_project
from src.utils.data_generator import DataGenerator
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils


app = dash.Dash(__name__)

json_storage = Constants.FilePaths.PROJECTS_DATA_JSON_PATH
data_mapper_instance = DataMapper(filename=json_storage)
idproj_prefix = "idproj_"


@callback(
    Output("rp--project-id", "value"),
    Input("rp--generate-id-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_random_id(n_clicks):
    return idproj_prefix + DataGenerator.generate_aggregated_uuid(length_threshold=5)


@callback(
    [
        Output("rp--output-message-projects", "children"),
        Output("rp--delete-output-message-projects", "children"),
        Output("rp--project-id", "value", allow_duplicate=True),
    ],
    [
        Input("rp--save-button", "n_clicks"),
        Input("rp--update-button", "n_clicks"),
        Input("rp--delete-button", "n_clicks"),
    ],
    [
        State("rp--project-id", "value"),
        State("rp--project-name", "value"),
        State("rp--delete-project-id", "value"),
    ],
    prevent_initial_call='initial_duplicate'
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    project_id,
    project_name,
    delete_project_id,
):

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rp--save-button":
            is_valid, message = ValidationUtils.validate_mandatory_fields(
                project_id=project_id,
                project_name=project_name
            )
            if not is_valid:
                return message, dash.no_update, dash.no_update

            try:
                data = data_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            new_data = {
                Constants.ProjectDataJSON.PROJECT_ID: project_id,
                Constants.ProjectDataJSON.PROJECT_NAME: project_name,
            }
            data[project_id] = new_data

            data_mapper_instance.save_to_json_storage(data)
            
            new_id = idproj_prefix + DataGenerator.generate_aggregated_uuid(length_threshold=5)

            return "Project saved successfully", dash.no_update, new_id

        case "rp--update-button":
            try:
                data = data_mapper_instance.load_from_json_storage()
            except FileNotFoundError:
                return dash.no_update, "No data found. Nothing to update.", dash.no_update

            if project_id in data:
                data[project_id][Constants.ProjectDataJSON.PROJECT_NAME] = project_name

                data_mapper_instance.save_to_json_storage(data)

                return "Project updated successfully", dash.no_update, dash.no_update
            else:
                return (
                    dash.no_update,
                    f'Data with project ID "{project_id}" not found in JSON. Nothing to update.',
                    dash.no_update,
                )

        case "rp--delete-button":
            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_project_id in data:
                    del data[delete_project_id]

                    data_mapper_instance.save_to_json_storage(data)

                    return (
                        dash.no_update,
                        f'Project with test name "{delete_project_id} - {project_name}" deleted successfully',
                        dash.no_update,
                    )
                else:
                    return (
                        dash.no_update,
                        f'Project with test name "{delete_project_id}" not found in JSON',
                        dash.no_update,
                    )
            except FileNotFoundError:
                return dash.no_update, "No data found. Nothing to delete.", dash.no_update

        case _:
            return "Please choose an action", dash.no_update, dash.no_update


app.layout = html_register_project.render_layout()
