import dash
from dash import html
import src.views.qpi_dashboard as dashboard
import src.views.qpi_register_testing_efforts as register
import src.views.dom.html_register_testing_efforts as html_register_efforts

def display_page_callback(pathname):
    match pathname:
        case "/register_tests":
            return register.html_register_efforts.render_layout()
        case "/dashboard":
            return dashboard.render_layout()
        case default:
            return html.Div("404 - Page not found")
