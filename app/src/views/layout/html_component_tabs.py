import random
import string
from dash import dcc, html
from src.utils.assets_handler import AssetsHandler
import src.controllers.app_path_config as app_path_config


decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def get_page_tabs_info():
    return [
        {
            "identifier": "dashboard",
            "route": "/dashboard",
            "tab_title": "Analytics KPI",
            "page_title": "KPIs",
        },
        {
            "identifier": "projects",
            "route": "/register_projects",
            "tab_title": "Register a project",
            "page_title": "Project",
        },
        {
            "identifier": "features",
            "route": "/register_features",
            "tab_title": "Register a feature",
            "page_title": "Feature",
        },
        {
            "identifier": "test_efforts",
            "route": "/register_tests",
            "tab_title": "Register a test efforts",
            "page_title": "Testing Efforts",
        }
    ]


def render_logo():
    return html.Img(
        src=decoded_logo_img,
        className="qpi_logo",
    )


def render_page_title(current_page_identifier=""):
    page_title = next(
        (
            page["page_title"]
            for page in get_page_tabs_info()
            if current_page_identifier == page["identifier"]
        ),
        "",
    )
    return html.H1(page_title)


def render_tabs(active_tab_identifier=""):
    dynamic_tabs = [
        dcc.Link(
            tab["tab_title"],
            href=tab["route"],
            className=f'tab--{"selected" if active_tab_identifier == tab["identifier"] else "unselected"}',
        )
        for tab in get_page_tabs_info()
    ]

    return html.Div(
        className="tabs",
        children=dynamic_tabs,
    )
