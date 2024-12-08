import dash
from dash import dcc, html
import src.views.qpi_dashboard_callback as dashboard
import src.views.qpi_register_efforts_callback as register_tests
import src.views.qpi_register_projects_callback as register_projects

# import src.views.qpi_register_features_callback as register_features

def display_page_callback(pathname):
    match pathname:
        case "/register_projects":
            return register_projects.html_register_project.render_layout()
        # case "/register_features":
        #     return register_features.html_register_features.render_layout()
        case "/register_tests":
            return register_tests.html_register_efforts.render_layout()
        case "/dashboard":
            return dashboard.html_dashboard.render_layout()
        case default:
            return html.Div("404 - Page not found")
