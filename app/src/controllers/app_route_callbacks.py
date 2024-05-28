import dash
from dash import html
import src.views.qpi_dashboard as dashboard
import src.views.qpi_register_testing_efforts as register

def display_page_callback(pathname):
    match pathname:
        case "/register_tests":
            return register.register_testing_efforts_layout
        case "/dashboard":
            return dashboard.serve_layout()
        case default:
            return html.Div("404 - Page not found")
