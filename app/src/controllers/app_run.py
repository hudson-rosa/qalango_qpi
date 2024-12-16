import dash
import app_path_config
from dash import html, callback
from dash.dependencies import Input, Output

app_path_config.set_current_dir(__file__)
from src.utils.constants.constants import Constants
from app_route_callbacks import display_page_callback


external_stylesheets = [
    Constants.FilePaths.DASHBOARD_STYLESHEET_CSS_PATH,
    Constants.FilePaths.FORMS_STYLESHEET_CSS_PATH,
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [dash.dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return display_page_callback(pathname)


if __name__ == "__main__":
    app.config.suppress_callback_exceptions = True
    print("Open the QPI Dashboard in the browser: http://127.0.0.1:8050/dashboard")
    app.run_server(debug=True)
