from dash import dcc, html


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


def render_layout():
    return html.Div(
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
                                    dcc.Dropdown(
                                        options=[
                                            {"label": "Unit", "value": "unit"},
                                            {
                                                "label": "Integration",
                                                "value": "integration",
                                            },
                                            {
                                                "label": "Component",
                                                "value": "component",
                                            },
                                            {"label": "Contract", "value": "contract"},
                                            {"label": "API", "value": "api"},
                                            {"label": "End-To-End", "value": "e2e"},
                                            {
                                                "label": "Performance (Load, Stress)",
                                                "value": "performance",
                                            },
                                            {"label": "Security", "value": "security"},
                                            {
                                                "label": "Usability",
                                                "value": "usability",
                                            },
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
                                            {
                                                "label": "Automated",
                                                "value": "automated",
                                            },
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
                                        id="delete-output-message",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="delete-test-name",
                                        type="text",
                                        placeholder="Enter test name to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
