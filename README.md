# GETTING STARTED

## INSTALLATION
Install all the dependencies and ensure the python environment is properly set by running this command:

```bash
    python3 setup_requirements.py
```

## RUNNING THE QPI DASHBOARD
Once the environment is ready for usage, run the QPI App via command line:

```bash
    python3 app/src/controllers/app_run.py
```

In a browser, open the QPI Dashboard from the URL:

(QPI DASHBOARD LOCALHOST)[http://127.0.0.1:8050/dashboard]

## RUNNING THE TESTS
For isntance, you can run the unit tests through this simple command:

```bash
    pytest
```

For further configurations, please, adjust the `pytest.ini` file.

# ISSUES
## MODULES NOT FOUND
If you are issues to run the tests, for example "ImportError" for the Modules imported within the test files, then make sure the PYTHONPATH env variable is already set with the intended project module "/app".

It can be exported directly via terminal:

```bash
    export PYTHONPATH=/absolute/path/to/qpi_dashboard/app:$PYTHONPATH
```

Or, the tests can be directly triggered with the env variables set via bash script file `sh pytest_env.sh` or even the Python file `run_pytest_with_vars.py`:

```bash
    sh run_pytest_with_vars.sh
    python3 run_pytest_with_vars.py
```