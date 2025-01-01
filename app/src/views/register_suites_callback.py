import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_suite as html_register_suite
from src.utils.data_generator import DataGenerator
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils
from src.models.mapper.project_mapper import ProjectMapper
from src.utils.string_handler import StringHandler


app = dash.Dash(__name__)

project_mapper_instance = ProjectMapper(Constants.FilePaths.PROJECTS_DATA_JSON_PATH)
json_storage = Constants.FilePaths.SUITES_DATA_JSON_PATH
data_mapper_instance = DataMapper(filename=json_storage)
idsuite_prefix = "idsuite_"


@callback(
    Output("rsu--suite-id", "value"),
    Input("rsu--generate-id-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_random_id(n_clicks):
    return idsuite_prefix + DataGenerator.generate_aggregated_uuid(length_threshold=5)


@callback(
    [
        Output("rsu--output-message-suites", "children"),
        Output("rsu--delete-output-message-suites", "children"),
        Output("rsu--suite-id", "value", allow_duplicate=True),
    ],
    [
        Input("rsu--save-button", "n_clicks"),
        Input("rsu--update-button", "n_clicks"),
        Input("rsu--delete-button", "n_clicks"),
    ],
    [
        State("rsu--project-dropdown", "value"),
        State("rsu--suite-id", "value"),
        State("rsu--suite-name", "value"),
        State("rsu--delete-suite-id", "value"),
    ],
    prevent_initial_call="initial_duplicate",
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    project_ref,
    suite_id,
    suite_name,
    delete_suite_id,
):
    ctx = dash.callback_context
    button_id = ValidationUtils.identify_triggering_action(callback_context=ctx)

    # Refresh Suite ID if not loaded
    if suite_id is None:
        suite_id = idsuite_prefix + DataGenerator.generate_aggregated_uuid()

    validation_rules = [
        (not project_ref, Constants.Messages.PROJECT_REFERENCE_IS_REQUIRED),
        (not suite_name, Constants.Messages.SUITE_NAME_IS_REQUIRED),
    ]

    match button_id:
        case "rsu--save-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.SUITE_SUITE_ID_IS_CREATED.format(
                        suite_id=suite_id
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

            project_id = StringHandler.get_id_format(project_ref)
            project_name = StringHandler.get_name_format(project_ref)

            new_suite = {
                Constants.SuiteDataJSON.SUITE_ID: suite_id,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
                Constants.ProjectDataJSON.PROJECT_REF: project_ref,
            }

            if project_id not in data:
                data[project_id] = {
                    Constants.ProjectDataJSON.PROJECT_NAME: project_name,
                    "suites": [],
                }

            data[project_id]["suites"].append(new_suite)

            data_mapper_instance.save_to_json_storage(data)

            new_id = idsuite_prefix + DataGenerator.generate_aggregated_uuid(
                length_threshold=5
            )

            return validation_message, dash.no_update, new_id

        case "rsu--update-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.SUITE_SUITE_ID_IS_UPDATED.format(
                        suite_id=suite_id
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

            if suite_id in data:
                data[suite_id][Constants.SuiteDataJSON.SUITE_NAME] = suite_name

                data_mapper_instance.save_to_json_storage(data)

                return (
                    validation_message,
                    dash.no_update,
                    dash.no_update,
                )
            else:
                return (
                    dash.no_update,
                    Constants.Messages.DATA_WITH_SUITE_ID_NOT_FOUND_IN_JSON_NOTHING_TO_UPDATE.format(
                        suite_id=suite_id
                    ),
                    dash.no_update,
                )

        case "rsu--delete-button":
            is_valid, validation_message = (
                ValidationUtils.validate_mandatory_field_rules(
                    Constants.Messages.SUITE_SUITE_ID_IS_DELETED.format(
                        suite_id=suite_id
                    ),
                    validation_rules,
                )
            )
            if not is_valid:
                return validation_message, dash.no_update, dash.no_update

            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_suite_id in data:
                    del data[delete_suite_id]

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


app.layout = html_register_suite.render_layout()
