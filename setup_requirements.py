import os
import run_pytest_with_vars

SEP = os.sep


def run_updates():
    _ver3 = set_for_unix()

    print("\nUpdating PIP...")
    os.system(f"python3 -m pip install --upgrade pip")

    print("\nInstalling Python Environment...")
    os.system(f"python3 -m pip install pipenv")

    print("\nSetting a new Python Environment...")
    os.system(f"python3 -m venv venv")
    os.system(f"source venv/bin/activate")

    print("\nUpdating all packages and resources...")
    os.system(f"python3 -m pip install -r requirements.txt")

    print("\nPackages installed:")
    os.system(f"python3 -m pip list")

    print("\nExporting App path to PYTHONPATH env var:")
    app_path = f"{os.path.dirname(os.path.abspath(__file__))}/app"
    app_src_path = f"{os.path.dirname(os.path.abspath(__file__))}/app/src"
    run_pytest_with_vars.exportValueToPythonPath([app_path, app_src_path])


def set_for_unix():
    if os.name != "nt":
        return "3"

if __name__ == "__main__":
    run_updates()
