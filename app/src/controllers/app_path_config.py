import os, sys

@staticmethod
def set_current_dir(__file__):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return sys.path.append(app_dir)

@staticmethod
def get_data_storage_path():
    return "app/data/storage/manual_test_data.json"

@staticmethod
def get_dashboard_stylesheet_css_path():
    return "./static/dashboard_stylesheet.css"

@staticmethod
def get_forms_stylesheet_css_path():
    return "./static/forms_stylesheet.css"
