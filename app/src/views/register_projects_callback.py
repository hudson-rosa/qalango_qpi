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
    Output("rpj--project-id", "value"),
    Input("rpj--generate-id-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_random_id(n_clicks):
    return idproj_prefix + DataGenerator.generate_aggregated_uuid(length_threshold=5)


@callback(
    [
        Output("rpj--output-message-projects", "children"),
        Output("rpj--delete-output-message-projects", "children"),
        Output("rpj--project-id", "value", allow_duplicate=True),
    ],
    [
        Input("rpj--save-button", "n_clicks"),
        Input("rpj--update-button", "n_clicks"),
        Input("rpj--delete-button", "n_clicks"),
    ],
    [
        State("rpj--project-id", "value"),
        State("rpj--project-name", "value"),
        State("rpj--delete-project-id", "value"),
    ],
    prevent_initial_call="initial_duplicate",
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
    button_id = ValidationUtils.identify_triggering_action(callback_context=ctx)

    # Refresh Project ID if not loaded
    if project_id is None:
        project_id = idproj_prefix + DataGenerator.generate_aggregated_uuid()

    # Validation Rules as tuples
    validation_rules = [(not project_name, Constants.Messages.PROJECT_NAME_IS_REQUIRED)]

    match button_id:
        case "rpj--save-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.PROJECT_PROJECT_ID_IS_CREATED.format(
                        project_id=project_id
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, dash.no_update, dash.no_update

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

            new_id = idproj_prefix + DataGenerator.generate_aggregated_uuid(
                length_threshold=5
            )

            return validation_message, dash.no_update, new_id

        case "rpj--update-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.PROJECT_PROJECT_ID_IS_UPDATED.format(
                        project_id=project_id
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, dash.no_update, dash.no_update

            try:
                data = data_mapper_instance.load_from_json_storage()
            except FileNotFoundError:
                return (
                    dash.no_update,
                    Constants.Messages.NO_DATA_FOUND_NOTHING_TO_UPDATE,
                    dash.no_update,
                )

            if project_id in data:
                data[project_id][Constants.ProjectDataJSON.PROJECT_NAME] = project_name

                data_mapper_instance.save_to_json_storage(data)

                return validation_message, dash.no_update, dash.no_update
            else:
                return (
                    dash.no_update,
                    Constants.Messages.DATA_WITH_PROJECT_ID_NOT_FOUND_IN_JSON_NOTHING_TO_UPDATE.format(
                        project_id=project_id
                    ),
                    dash.no_update,
                )

        case "rpj--delete-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.PROJECT_PROJECT_ID_IS_DELETED.format(
                        project_id=project_id
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, dash.no_update, dash.no_update

            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_project_id in data:
                    del data[delete_project_id]

                    data_mapper_instance.save_to_json_storage(data)

                    return (
                        dash.no_update,
                        validation_message,
                        dash.no_update,
                    )
                else:
                    return (
                        dash.no_update,
                        validation_message,
                        dash.no_update,
                    )
            except FileNotFoundError:
                return (
                    dash.no_update,
                    Constants.Messages.NO_DATA_FOUND_NOTHING_TO_DELETE,
                    dash.no_update,
                )

        case _:
            return (
                Constants.Messages.PLEASE_FILL_IN_THE_FIELDS_BEFORE_CHOOSING_AN_ACTION,
                dash.no_update,
                dash.no_update,
            )


app.layout = html_register_project.render_layout()
