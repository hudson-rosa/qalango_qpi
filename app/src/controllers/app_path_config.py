import os, sys


@staticmethod
def set_current_dir(__file__):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return sys.path.append(app_dir)


def find_folder_in_path(start_path, folder_name):
    updated_current_path = os.path.dirname(start_path)
    while True:
        if folder_name in os.listdir(updated_current_path):
            return os.path.join(updated_current_path, folder_name)
        navigated_parent_directory = os.path.dirname(updated_current_path)

        if navigated_parent_directory == updated_current_path:
            raise FileNotFoundError(
                f"Folder '{folder_name}' not found in path '{start_path}'"
            )
        updated_current_path = navigated_parent_directory

        return updated_current_path
