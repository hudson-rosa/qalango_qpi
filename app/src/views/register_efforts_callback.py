import dash
import json
from dash import dcc, callback, html, Input, Output, State
from src.models.mapper.data_mapper import DataMapper

import src.views.layout.html_register_testing_efforts as html_register_efforts
from src.utils.constants.constants import Constants
from src.utils.validation_utils import ValidationUtils


app = dash.Dash(__name__)

json_storage = Constants.FilePaths.TEST_EFFORTS_DATA_JSON_PATH
test_efforts_data_mapper_instance = DataMapper(filename=json_storage)


@callback(
    dash.dependencies.Output("slider-output", "children"),
    [dash.dependencies.Input("total-time", "value")],
)
def update_output(value):
    hours = value // 60
    minutes = value % 60
    return f"Selected time: {hours}:{minutes:02d}"


@callback(
    [
        Output("rte--output-message", "children"),
        Output("rte--delete-output-message", "children"),
    ],
    [
        Input("rte--save-button", "n_clicks"),
        Input("rte--update-button", "n_clicks"),
        Input("rte--delete-button", "n_clicks"),
    ],
    [
        State("rte--test-name", "value"),
        State("rte--suite-name", "value"),
        State("rte--project-name", "value"),
        State("rte--total-time", "value"),
        State("rte--delete-test-name", "value"),
        State("rte--test-level", "value"),
        State("rte--test-approach", "value"),
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    test_name,
    suite_name,
    project_name,
    total_time,
    delete_test_name,
    test_level,
    test_approach,
):
    ctx = dash.callback_context
    button_id = ValidationUtils.identify_triggering_action(callback_context=ctx)

    match button_id:
        case "rte--save-button":
            try:
                data = test_efforts_data_mapper_instance.load_from_json_storage()

            except (FileNotFoundError, json.decoder.JSONDecodeError):
                data = {}

            new_data = {
                Constants.ScenariosDataJSON.TEST_NAME: test_name,
                Constants.ScenariosDataJSON.SUITE_NAME: suite_name,
                Constants.ProjectDataJSON.PROJECT_NAME: str(project_name)
                .split("(")[1]
                .rstrip(")"),
                Constants.ScenariosDataJSON.TOTAL_TIME: total_time,
                Constants.ScenariosDataJSON.TEST_LEVEL: test_level,
                Constants.ScenariosDataJSON.TEST_APPROACH: test_approach,
            }
            data[test_name] = new_data

            test_efforts_data_mapper_instance.save_to_json_storage(new_data=data)

            return "Data saved successfully", None

        case "rte--update-button":
            try:
                data = test_efforts_data_mapper_instance.load_from_json_storage()

            except FileNotFoundError:
                return None, "No data found. Nothing to update."

            if test_name in data:
                data[test_name][Constants.ScenariosDataJSON.SUITE_NAME] = suite_name
                data[test_name][Constants.ScenariosDataJSON.PROJECT_NAME] = project_name
                data[test_name][Constants.ScenariosDataJSON.TOTAL_TIME] = total_time
                data[test_name][Constants.ScenariosDataJSON.TEST_LEVEL] = test_level
                data[test_name][
                    Constants.ScenariosDataJSON.TEST_APPROACH
                ] = test_approach

                test_efforts_data_mapper_instance.save_to_json_storage(new_data=data)

                return "Data updated successfully", None
            else:
                return (
                    None,
                    f'Data with test name "{test_name}" not found in JSON. Nothing to update.',
                )

        case "rte--delete-button":
            try:
                data = test_efforts_data_mapper_instance.load_from_json_storage()

                if delete_test_name in data:
                    del data[delete_test_name]

                    test_efforts_data_mapper_instance.save_to_json_storage(
                        new_data=data
                    )

                    return (
                        None,
                        f'Data with test name "{delete_test_name}" deleted successfully',
                    )
                else:
                    return (
                        None,
                        f'Data with test name "{delete_test_name}" not found in JSON',
                    )
            except FileNotFoundError:
                return None, "No data found. Nothing to delete."

        case _:
            return "Please choose an action", None


app.layout = html_register_efforts.render_layout()
