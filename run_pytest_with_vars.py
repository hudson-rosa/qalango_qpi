import os, sys

app_path = f"{os.path.dirname(os.path.abspath(__file__))}/app"
app_src_path = f"{os.path.dirname(os.path.abspath(__file__))}/app/src"


def main():
    clean_bashrc()
    exportValueToPythonPath(app_paths=[app_path, app_src_path])
    print_file_content()
    os.system(f"pytest")


def exportValueToPythonPath(app_paths=[os.path.dirname(os.path.abspath(__file__))]):
    os.environ["PYTHONPATH"] = ""
    python_path = os.environ.get("PYTHONPATH")

    for path_value in app_paths:
        if python_path is not None:
            os.environ["PYTHONPATH"] = (
                f"{path_value}:{os.environ.get('PYTHONPATH', '')}"
            )
            os.system(f"export PYTHONPATH={path_value}:$PYTHONPATH")
            print(f"PYTHONPATH = {path_value}")

    updated_pythonpath = os.environ.get("PYTHONPATH", "")
    print("The PYTHONPATH is set with:", updated_pythonpath)

    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as bashrc_file:
        bashrc_file.write(f'export PYTHONPATH="{updated_pythonpath}"\n')

    os.system("source")


def clean_bashrc(file_path="~/.bashrc"):
    bashrc_path = os.path.expanduser(file_path)
    with open(bashrc_path, "w") as file_to_clean:
        file_to_clean.truncate(0)
    print(f"Cleared contents of {bashrc_path}")


def print_file_content(file_path="~/.bashrc"):
    os.system(f"cat {file_path}")


if __name__ == "__main__":
    main()
