from dash import dcc, html
from src.utils.assets_handler import AssetsHandler
from src.utils.constants.constants import Constants


decoded_logo_img = AssetsHandler(Constants.FilePaths.QPI_LOGO_PNG_PATH).decode_base64()


def get_page_tabs_info():
    return [
        {
            "identifier": Constants.PageIdentifiers.DASHBOARD,
            "route": Constants.Routes.DASHBOARD,
            "tab_title": "Coverage KPI",
            "page_title": "Test Coverage KPIs",
        },
        {
            "identifier": Constants.PageIdentifiers.PROJECTS,
            "route": Constants.Routes.REGISTER_PROJECTS,
            "tab_title": "Register project",
            "page_title": "Projects",
        },
        {
            "identifier": Constants.PageIdentifiers.FEATURES,
            "route": Constants.Routes.REGISTER_FEATURES,
            "tab_title": "Register feature",
            "page_title": "BDD Features",
        },
        {
            "identifier": Constants.PageIdentifiers.TEST_EFFORTS,
            "route": Constants.Routes.REGISTER_TESTS,
            "tab_title": "Register test efforts",
            "page_title": "Testing Efforts",
        },
    ]


def render_logo():
    return html.Div(
        className="header-group logo-container",
        children=[
            html.Img(
                src=decoded_logo_img,
                className="qpi-logo",
            )
        ],
    )


def render_page_title(current_page_identifier=""):
    page_title = next(
        (
            page["page_title"]
            for page in get_page_tabs_info()
            if current_page_identifier == page["identifier"]
        )
    )
    return html.Div(
        className="header-group title-container",
        children=[html.H1(page_title)],
    )


def render_header(current_page_identifier=""):
    return html.Div(
        className="grid-container",
        children=[
            render_logo(),
            render_page_title(current_page_identifier),
        ],
    )


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