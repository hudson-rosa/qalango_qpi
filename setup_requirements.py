import os
import run_pytest_with_vars

SEP = os.sep


def run_updates():
    _v3 = set_for_unix()

    print("\nUpdating PIP...")
    
    os.system(f"deactivate")
    os.system(f"rm -rf .venv venv")
    os.system(f"python{_v3} -m venv venv")
    os.system(f"source venv/bin/activate")

    print("\nUpdating all packages and resources...")
    os.system(f"python{_v3} -m pip install --upgrade pip")
    os.system(f"pip install -r requirements.txt")
    os.system(f"pip install playwright")
    os.system(f"playwright install --with-deps")

    print("\nPackages installed:")
    os.system(f"which python")
    os.system(f"which pip")
    os.system(f"pip list")

    print("\nExporting App path to PYTHONPATH env var:")
    app_path = f"{os.path.dirname(os.path.abspath(__file__))}/app"
    app_src_path = f"{os.path.dirname(os.path.abspath(__file__))}/app/src"
    run_pytest_with_vars.exportValueToPythonPath([app_path, app_src_path])


def set_for_unix():
    if os.name != "nt":
        return "3.11"

if __name__ == "__main__":
    run_updates()
