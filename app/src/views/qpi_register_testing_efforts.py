import dash
import json
import src.controllers.app_path_config as app_path_config
import src.views.dom.html_register_testing_efforts as html_register_efforts
from dash import dcc, callback, html, Input, Output, State
import dash_daq as daq

app = dash.Dash(__name__)

json_storage = app_path_config.get_data_storage_path()


def generate_marks():
    marks = {}
    step_size = 15
    num_intervals = 30

    # First 5 minutes: steps of 1 minute
    for i in range(0, 6, 1):
        marks[i] = f"{i%60:01d}"

    # Subsequent 15 minutes: steps of 3 minutes
    for i in range(6, 16, 3):
        marks[i] = f"{i%60:01d}"

    # Subsequent minutes until 3 hours: steps of 15 minutes
    for i in range(num_intervals + 1):
        time_in_minutes = i * step_size
        hours = time_in_minutes // 60
        minutes = time_in_minutes % 60
        marks[time_in_minutes] = f"{hours}:{minutes:02d}"

    return marks


slider_marks = generate_marks()


@callback(
    dash.dependencies.Output("slider-output", "children"),
    [dash.dependencies.Input("total-time", "value")],
)
def update_output(value):
    hours = value // 60
    minutes = value % 60
    return f"Selected time: {hours}:{minutes:02d}"


@callback(
    [Output("output-message", "children"), Output("delete-output-message", "children")],
    [
        Input("save-button", "n_clicks"),
        Input("update-button", "n_clicks"),
        Input("delete-button", "n_clicks"),
    ],
    [
        State("test-name", "value"),
        State("test-suite", "value"),
        State("project-name", "value"),
        State("total-time", "value"),
        State("delete-test-name", "value"),
        State("test-category", "value"),
        State("test-approach", "value"),
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    test_name,
    test_suite,
    project_name,
    total_time,
    delete_test_name,
    test_category,
    test_approach
):

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = str(ctx.triggered[0]["prop_id"]).split(".")[0]

    if button_id == "save-button":
        try:
            with open(json_storage, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        new_data = {
            "test_name": test_name,
            "test_suite": test_suite,
            "project_name": project_name,
            "total_time": total_time,
            "test_category": test_category,
            "test_approach": test_approach
        }
        data[test_name] = new_data

        with open(json_storage, "w") as f:
            json.dump(data, f)

        return "Data saved successfully", None

    elif button_id == "update-button":
        try:
            with open(json_storage, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return None, "No data found. Nothing to update."

        if test_name in data:
            data[test_name]["test_suite"] = test_suite
            data[test_name]["project_name"] = project_name
            data[test_name]["total_time"] = total_time
            data[test_name]["test_category"] = test_category
            data[test_name]["test_approach"] = test_approach

            with open(json_storage, "w") as f:
                json.dump(data, f)

            return "Data updated successfully", None
        else:
            return (
                None,
                f'Data with test name "{test_name}" not found in JSON. Nothing to update.',
            )

    elif button_id == "delete-button":
        try:
            with open(json_storage, "r") as f:
                data = json.load(f)
            if delete_test_name in data:
                del data[delete_test_name]
                with open(json_storage, "w") as f:
                    json.dump(data, f)
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

    else:
        return "Please choose an action", None


app.layout = html_register_efforts.render_layout()
