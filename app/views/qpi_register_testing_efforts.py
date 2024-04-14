import dash
import json
from dash import dcc, callback, html, Input, Output, State

app = dash.Dash(__name__)

manual_test_data_json = "data/storage/manual_test_data.json"

register_testing_efforts_layout = html.Div(
    [
        html.H1("Registering Testing Efforts Page"),
        dcc.Link("Go to Dashboard", href="/dashboard"),
        html.Div(
            [
                html.Label("Test Name"),
                dcc.Input(id="test-name", type="text", placeholder="Enter test name"),
                html.Label("Test Suite"),
                dcc.Input(id="test-suite", type="text", placeholder="Enter test suite"),
                html.Label("Test Category"),
                dcc.Input(
                    id="test-category", type="text", placeholder="Enter test category"
                ),
                html.Label("Total Time (in minutes)"),
                dcc.Input(
                    id="total-time", type="number", placeholder="Enter total time"
                ),
                html.Div(
                    [
                        html.Button("Save", id="save-button", n_clicks=0),
                        html.Button("Update", id="update-button", n_clicks=0),
                        html.Button("Delete", id="delete-button", n_clicks=0),
                    ]
                ),
                html.Div(id="output-message"),
            ]
        ),
        html.Div(
            [
                html.Label("Test Name to delete"),
                dcc.Input(
                    id="delete-test-name",
                    type="text",
                    placeholder="Enter test name to delete",
                ),
                html.Div(id="delete-output-message"),
            ]
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
            with open(manual_test_data_json, "r") as f:
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

        with open(manual_test_data_json, "w") as f:
            json.dump(data, f)

        return "Data saved successfully", None

    elif button_id == "update-button":
        try:
            with open(manual_test_data_json, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return None, "No data found. Nothing to update."

        if test_name in data:
            data[test_name]["test_suite"] = test_suite
            data[test_name]["test_category"] = test_category
            data[test_name]["total_time"] = total_time

            with open(manual_test_data_json, "w") as f:
                json.dump(data, f)

            return "Data updated successfully", None
        else:
            return (
                None,
                f'Data with test name "{test_name}" not found in JSON. Nothing to update.',
            )

    elif button_id == "delete-button":
        try:
            with open(manual_test_data_json, "r") as f:
                data = json.load(f)
            if delete_test_name in data:
                del data[delete_test_name]
                with open(manual_test_data_json, "w") as f:
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
        return "Please select an action from the dropdown", None


app.layout = register_testing_efforts_layout
