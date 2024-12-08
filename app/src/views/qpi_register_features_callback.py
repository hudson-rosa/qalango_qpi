import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.controllers.app_path_config as app_path_config
import src.views.layout.html_register_feature as html_register_feature
from src.utils.data_generator import DataGenerator
import dash_daq as daq

app = dash.Dash(__name__)

json_storage = app_path_config.get_data_storage_projects_path()
data_mapper_instance = DataMapper(filename=json_storage)


@callback(
    Output("rp--feature-id", "value"),
    Input("rp--generate-id-button", "n_clicks"),
    prevent_initial_call=False
)
def update_random_id(n_clicks):
    return "idfeat_" + DataGenerator.generate_aggregated_uuid()

@callback(
    [Output("rp--output-message-features", "children"), Output("rp--delete-output-message-features", "children")],
    [
        Input("rp--save-button", "n_clicks"),
        Input("rp--update-button", "n_clicks"),
        Input("rp--delete-button", "n_clicks"),
    ],
    [
        State("rp--feature-id", "value"),
        State("rp--feature-name", "value"),
        State("rp--delete-feature-id", "value")
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    feature_id,
    feature_name,
    delete_feature_id
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
                "feature_id": feature_id,
                "feature_name": feature_name
            }
            data[feature_id] = new_data

            data_mapper_instance.save_to_json_storage(data)

            return "Feature saved successfully", None

        case "rp--update-button":
            try:
                data = data_mapper_instance.load_from_json_storage()
            except FileNotFoundError:
                return None, "No data found. Nothing to update."

            if feature_id in data:
                data[feature_id]["feature_name"] = feature_name

                data_mapper_instance.save_to_json_storage(data)

                return "Feature updated successfully", None
            else:
                return (
                    None,
                    f'Data with feature ID "{feature_id}" not found in JSON. Nothing to update.',
                )

        case "rp--delete-button":
            try:
                data = data_mapper_instance.load_from_json_storage()

                if delete_feature_id in data:
                    del data[delete_feature_id]

                    data_mapper_instance.save_to_json_storage(data)

                    return (
                        None,
                        f'Feature with test name "{delete_feature_id} - {feature_name}" deleted successfully',
                    )
                else:
                    return (
                        None,
                        f'Feature with test name "{delete_feature_id}" not found in JSON',
                    )
            except FileNotFoundError:
                return None, "No data found. Nothing to delete."

        case _:
            return "Please choose an action", None


app.layout = html_register_feature.render_layout()
