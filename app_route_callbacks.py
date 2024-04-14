import dash
from dash import html
import qpi_dashboard as dashboard
import qpi_register_testing_efforts as register


def display_page_callback(pathname):
    match pathname:
        case "/register_tests":
            return register.register_testing_efforts_layout
        case "/dashboard":
            return dashboard.dashboard_layout
        case default:
            return html.Div("404 - Page not found")
