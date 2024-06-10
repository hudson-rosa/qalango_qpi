import dash
from dash import html
import src.views.qpi_dashboard_callback as dashboard
import src.views.qpi_register_efforts_callback as register

def display_page_callback(pathname):
    match pathname:
        case "/register_tests":
            return register.html_register_efforts.render_layout()
        case "/dashboard":
            return dashboard.html_dashboard.render_layout()
        case default:
            return html.Div("404 - Page not found")
