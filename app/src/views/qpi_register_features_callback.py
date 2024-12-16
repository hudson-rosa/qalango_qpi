import dash
import json

from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_feature as html_register_feature
from src.utils.data_generator import DataGenerator
from src.utils.file_handler import FileHandler
from src.utils.constants.constants import Constants


app = dash.Dash(__name__)

features_json_storage = Constants.FilePaths.FEATURES_DATA_JSON_PATH
features_mapper_instance = DataMapper(filename=features_json_storage)


@callback(
    Output("rf--feature-id", "value"),
    Input("rf--generate-id-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_random_id(n_clicks):
    return "idfeat_" + DataGenerator.generate_aggregated_uuid()


@callback(
    Output("rf--output-message", "children"),
    [
        Input("rf--submit-bdd-button", "n_clicks"),
        Input("rf--delete-file-button", "n_clicks"),
    ],
    [
        State("rf--feature-id", "value"),
        State("rf--feature-name", "value"),
        State("rf--bdd-editor", "value"),
    ],
)
def save_update_delete_data(
    submit_clicks,
    delete_file_clicks,
    feature_id,
    feature_name="undefined",
    bdd_content=None,
):
    ctx = dash.callback_context
    feature_name_edited = str(feature_name).strip().replace(" ", "_")
    feature_file_pathname = f"{Constants.Folders.FEATURES_FOLDER}/{feature_id}--{feature_name_edited.lower()}.feature"

    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    match button_id:
        case "rf--submit-bdd-button":
            try:
                data = features_mapper_instance.load_from_json_storage()
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}
                
            bdd_content_lower = str(bdd_content).lower()
            new_data = {
                Constants.FeaturesDataJSON.FEATURE_ID: feature_id,
                Constants.FeaturesDataJSON.FEATURE_NAME: feature_name_edited,
                Constants.FeaturesDataJSON.QTY_OF_SCENARIOS: bdd_content_lower.count("scenario:") + bdd_content_lower.count("scenario outline:"),
                Constants.FeaturesDataJSON.QTY_OF_INTEGRATION: bdd_content_lower.count("@integration"),
                Constants.FeaturesDataJSON.QTY_OF_COMPONENT: bdd_content_lower.count("@component"),
                Constants.FeaturesDataJSON.QTY_OF_CONTRACT: bdd_content_lower.count("@contract"),
                Constants.FeaturesDataJSON.QTY_OF_API: bdd_content_lower.count("@api"),
                Constants.FeaturesDataJSON.QTY_OF_E2E: bdd_content_lower.count("@e2e"),
                Constants.FeaturesDataJSON.QTY_OF_PERFORMANCE: bdd_content_lower.count("@performance"),
                Constants.FeaturesDataJSON.QTY_OF_SECURITY: bdd_content_lower.count("@security"),
                Constants.FeaturesDataJSON.QTY_OF_USABILITY: bdd_content_lower.count("@usability"),
                Constants.FeaturesDataJSON.QTY_OF_EXPLORATORY: bdd_content_lower.count("@exploratory"),
                Constants.FeaturesDataJSON.QTY_OF_AUTOMATED: bdd_content_lower.count("@automated"),
            }
            data[feature_id] = new_data

            features_mapper_instance.save_to_json_storage(data)

            FileHandler.save_new_file(
                file_pathname=feature_file_pathname, content=bdd_content
            )

            return (
                html.Pre(f"BDD Feature saved successfully:\n\n{feature_file_pathname}"),
                None,
            )

        case "rf--delete-file-button":
            try:
                data = features_mapper_instance.load_from_json_storage()

                FileHandler.delete_file(feature_file_pathname)

                if feature_id in data:
                    del data[feature_id]

                    features_mapper_instance.save_to_json_storage(data)

                    return (
                        None,
                        f"Feature file deleted successfully",
                    )
                else:
                    return (
                        None,
                        f"Feature file was not found",
                    )
            except FileNotFoundError:
                return None, "Deletion not possible. The JSON file was not found."

        case _:
            return "Please choose an action", None


app.layout = html_register_feature.render_layout()
