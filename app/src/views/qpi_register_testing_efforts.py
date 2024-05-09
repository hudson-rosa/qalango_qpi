import dash
import json
import src.controllers.app_path_config as app_path_config
from dash import dcc, callback, html, Input, Output, State

app = dash.Dash(__name__)

json_storage = app_path_config.get_data_storage_path()

register_testing_efforts_layout = html.Div(
    [
        html.H1("Registering Testing Efforts Page"),
        dcc.Link("Go to Dashboard", href="/dashboard"),
        html.Div(
            className="form-content",
            children=[
                html.Ul(
                    html.Li(
                        html.Div(
                            className="grid grid-2",
                            children=[
                                dcc.Input(
                                    id="test-name",
                                    type="text",
                                    placeholder="Enter test name",
                                    required=True,
                                ),
                                dcc.Input(
                                    id="test-suite",
                                    type="text",
                                    placeholder="Enter test suite",
                                    required=True,
                                ),
                                dcc.Input(
                                    id="test-category",
                                    type="text",
                                    placeholder="Enter test category",
                                    required=True,
                                ),
                                dcc.Input(
                                    id="total-time",
                                    type="number",
                                    placeholder="Enter total execution time (in minutes)",
                                ),
                            ],
                        )
                    )
                ),
                html.Label("Required fields", className="required-msg"),
                html.Div(id="output-message", className="output-msg"),
                html.Div(
                    className="grid grid-2",
                    children=[
                        html.Button("Save", id="save-button", n_clicks=0),
                        html.Button("Update", id="update-button", n_clicks=0),
                        html.Div(
                            className="section-group",
                            children=[
                                html.Div(
                                    id="delete-output-message", className="output-msg"
                                ),
                                dcc.Input(
                                    id="delete-test-name",
                                    type="text",
                                    placeholder="Enter test name to delete",
                                ),
                                html.Button("Delete", id="delete-button", n_clicks=0),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)


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
        State("test-category", "value"),
        State("total-time", "value"),
        State("delete-test-name", "value"),
    ],
)
def save_update_delete_data(
    save_clicks,
    update_clicks,
    delete_clicks,
    test_name,
    test_suite,
    test_category,
    total_time,
    delete_test_name,
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
            "test_category": test_category,
            "total_time": total_time,
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
            data[test_name]["test_category"] = test_category
            data[test_name]["total_time"] = total_time

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


app.layout = register_testing_efforts_layout
