import dash
from dash import dcc, html
import src.views.dashboard_callback as dashboard
import src.views.register_efforts_callback as register_tests
import src.views.register_projects_callback as register_projects
import src.views.register_suites_callback as register_suites
import src.views.register_features_or_tests_callback as register_features
from src.utils.constants.constants import Constants


def display_page_callback(pathname):
    match pathname:
        case Constants.Routes.REGISTER_PROJECTS:
            return register_projects.html_register_project.render_layout()
        case Constants.Routes.REGISTER_SUITES:
            return register_suites.html_register_suite.render_layout()
        case Constants.Routes.REGISTER_SCENARIOS:
            return register_features.html_register_feature_or_tests.render_layout()
        case Constants.Routes.REGISTER_TESTS_EFFORTS:
            return register_tests.html_register_efforts.render_layout()
        case Constants.Routes.KPIS:
            return dashboard.html_dashboard.render_layout()
        case default:
            return html.Div("404 - Page not found")
