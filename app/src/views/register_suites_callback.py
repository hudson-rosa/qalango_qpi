import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_suite as html_register_suite
from src.utils.data_generator import DataGenerator
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils


app = dash.Dash(__name__)

json_storage = Constants.FilePaths.SUITES_DATA_JSON_PATH
data_mapper_instance = DataMapper(filename=json_storage)


@callback(
    Output("rs--suite-id", "value"),
    Input("rs--generate-id-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_random_id(n_clicks):
    return "idsuite_" + DataGenerator.generate_aggregated_uuid(length_threshold=5)


@callback(
    [
        Output("rs--output-message-suites", "children"),
        Output("rs--delete-output-message-suites", "children"),
    ],
    [
        Input("rs--save-button", "n_clicks"),
        Input("rs--update-button", "n_clicks"),
        Input("rs--delete-button", "n_clicks"),
    ],
    [
        State("rs--suite-id", "value"),
        State("rs--suite-name", "value"),
        State("rs--delete-suite-id", "value"),
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    suite_id,
    suite_name,
    delete_suite_id,
):

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rs--save-button":
            is_valid, message = ValidationUtils.validate_mandatory_fields(
                suite_id=suite_id,
                suite_name=suite_name
            )
            if not is_valid:
                return message, None

            try:
                data = data_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            new_data = {
                Constants.SuiteDataJSON.SUITE_ID: suite_id,
                Constants.SuiteDataJSON.SUITE_NAME: suite_name,
            }
            data[suite_id] = new_data

            data_mapper_instance.save_to_json_storage(data)

            return "Suite saved successfully", None

        case "rs--update-button":
            try:
                data = data_mapper_instance.load_from_json_storage()
            except FileNotFoundError:
                return None, "No data found. Nothing to update."

            if suite_id in data:
                data[suite_id][Constants.SuiteDataJSON.SUITE_NAME] = suite_name

                data_mapper_instance.save_to_json_storage(data)

                return "Suite updated successfully", None
            else:
                return (
                    None,
                    f'Data with Suite ID "{suite_id}" not found in JSON. Nothing to update.',
                )

        case "rs--delete-button":
            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_suite_id in data:
                    del data[delete_suite_id]

                    data_mapper_instance.save_to_json_storage(data)

                    return (
                        None,
                        f'Suite with test name "{delete_suite_id} - {suite_name}" deleted successfully',
                    )
                else:
                    return (
                        None,
                        f'Suite with test name "{delete_suite_id}" not found in JSON',
                    )
            except FileNotFoundError:
                return None, "No data found. Nothing to delete."

        case _:
            return "Please choose an action", None


app.layout = html_register_suite.render_layout()
