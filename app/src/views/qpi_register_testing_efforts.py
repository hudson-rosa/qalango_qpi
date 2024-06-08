import dash
import json
import src.controllers.app_path_config as app_path_config
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
                                    placeholder="Enter test title",
                                    required=True,
                                ),
                                dcc.Input(
                                    id="test-suite",
                                    type="text",
                                    placeholder="Enter test suite",
                                    required=True,
                                ),
                                dcc.Input(
                                    id="project-name",
                                    type="text",
                                    placeholder="Enter project name",
                                    required=True,
                                ),
                                # dcc.Input(
                                #     id="total-time",
                                #     type="number",
                                #     className="c_number_spinner",
                                #     placeholder="Enter total execution time (in minutes)",
                                # ),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Unit", "value": "unit"},
                                        {
                                            "label": "Integration",
                                            "value": "integration",
                                        },
                                        {"label": "Component", "value": "component"},
                                        {"label": "Contract", "value": "contract"},
                                        {"label": "API", "value": "api"},
                                        {"label": "End-To-End", "value": "e2e"},
                                        {
                                            "label": "Performance (Load, Stress)",
                                            "value": "performance",
                                        },
                                        {"label": "Security", "value": "security"},
                                        {"label": "Usability", "value": "usability"},
                                        {
                                            "label": "Exploratory",
                                            "value": "exploratory",
                                        },
                                    ],
                                    id="test-category",
                                    placeholder="Enter test category",
                                    searchable=True,
                                    className="c_dropdown",
                                    value="exploratory",
                                ),
                                html.Div(
                                    [
                                        html.H4("Enter total test execution time"),
                                        dcc.Slider(
                                            id="total-time",
                                            min=0,
                                            max=301,
                                            marks=slider_marks,
                                            step=None,
                                            value=0,
                                            included=False,
                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": True,
                                            },
                                            className="c_slider",
                                        ),
                                        html.H5(id="slider-output"),
                                    ]
                                ),
                                dcc.RadioItems(
                                    id="test-approach",
                                    options=[
                                        {"label": "Manual", "value": "manual"},
                                        {"label": "Automated", "value": "automated"},
                                    ],
                                    className="c_radio",
                                    value="manual",
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


app.layout = register_testing_efforts_layout
