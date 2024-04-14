import os, sys


def add_app_dir_to_path(current_dir):
    current_dir = (
        os.path.dirname(os.path.abspath(__file__))
        if current_dir is None
        else current_dir
    )
    app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

    sys.path.append(app_dir)
