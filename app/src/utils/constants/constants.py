class Constants:

    class Routes:
        KPIS = "/kpis"
        REGISTER_PROJECTS = "/register-projects"
        REGISTER_SCENARIOS = "/register-scenarios"
        REGISTER_SUITES = "/register-suites"
        REGISTER_TESTS_EFFORTS = "/register-test-efforts"

    class FeaturesDataJSON:
        FEATURE_ID = "feature_id"
        FEATURE_NAME = "feature_name"
        REQUIREMENTS_LINK = "requirements_link"
        QTY_OF_SCENARIOS = "qty_of_scenarios"
        QTY_OF_INTEGRATION = "qty_of_integration"
        QTY_OF_COMPONENT = "qty_of_component"
        QTY_OF_CONTRACT = "qty_of_contract"
        QTY_OF_API = "qty_of_api"
        QTY_OF_E2E = "qty_of_e2e"
        QTY_OF_PERFORMANCE = "qty_of_performance"
        QTY_OF_SECURITY = "qty_of_security"
        QTY_OF_USABILITY = "qty_of_usability"
        QTY_OF_EXPLORATORY = "qty_of_exploratory"
        QTY_OF_AUTOMATED = "qty_of_automated"
        QTY_OF_MANUAL = "qty_of_manual"
        QTY_OF_SMOKE_TESTS = "qty_of_smoke_tests"
        QTY_OF_EDGE_CASES = "qty_of_edge_cases"
        QTY_OF_CRITICAL_TESTS = "qty_of_critical_tests"
        QTY_OF_MOBILE = "qty_of_mobile"
        QTY_OF_DESKTOP = "qty_of_desktop"

    class ProjectDataJSON:
        PROJECT_ID = "project_id"
        PROJECT_NAME = "project_name"
        PROJECT_REF = "project_ref"

    class SuiteDataJSON:
        SUITE_ID = "suite_id"
        SUITE_NAME = "suite_name"
        SUITE_REF = "suite_ref"

    class ScenariosDataJSON:
        PROJECT_ID = "project_id"
        PROJECT_NAME = "project_name"
        SCENARIO_ID = "scenario_id"
        SCENARIO_NAME = "scenario_name"
        TEST_APPROACH = "test_approach"
        TEST_ID = "test_id"
        TEST_NAME = "test_name"
        TEST_LEVEL = "test_level"
        SUITE_NAME = "suite_name"
        TOTAL_TIME = "total_time"

    class TestCategoriesEntity:
        CRITICAL_TEST = "critical-test"
        SMOKE_TEST = "smoke-test"
        EDGE_CASE = "edge-case"
        MOBILE = "mobile"
        DESKTOP = "desktop"

    class TestLevelsEntity:
        UNIT = "unit"
        INTEGRATION = "integration"
        COMPONENT = "component"
        CONTRACT = "contract"
        API = "api"
        E2E = "e2e"
        PERFORMANCE = "performance"
        SECURITY = "security"
        USABILITY = "usability"
        EXPLORATORY = "exploratory"

    class TestTypesEntity:
        AUTOMATED = "automated"
        MANUAL = "manual"

    class FilePaths:
        DASHBOARD_STYLESHEET_CSS_PATH = "./static/dashboard_stylesheet.css"
        FORMS_STYLESHEET_CSS_PATH = "./static/forms_stylesheet.css"
        QALANGO_LOGO_PNG_PATH = "app/assets/images/Qalango_logo_transp.png"
        FEATURES_DATA_JSON_PATH = "app/data/storage/features_data.json"
        SCRIPTED_TESTS_DATA_JSON_PATH = "app/data/storage/test_cases_data.json"
        SCENARIOS_DATA_JSON_PATH = "app/data/storage/scenarios_data.json"
        PROJECTS_DATA_JSON_PATH = "app/data/storage/projects_data.json"
        SUITES_DATA_JSON_PATH = "app/data/storage/suites_data.json"
        TEST_EFFORTS_DATA_JSON_PATH = "app/data/storage/test_efforts_data.json"

    class Folders:
        FEATURES_FOLDER = "app/data/storage/features"
        TEST_CASES_FOLDER = "app/data/storage/test_cases"

    class PageIdentifiers:
        DASHBOARD = "dashboard"
        FEATURES = "features"
        PROJECTS = "projects"
        SUITES = "suites"
        TEST_EFFORTS = "test_efforts"

    class Messages:
        ALL_ADDED_PRECONDITIONS_NEED_TO_BE_FILLED_IN = (
            "All the added Preconditions need to be filled in."
        )
        ALL_ADDED_STEPS_NEED_TO_BE_FILLED_IN = (
            "All the added Steps need to be filled in."
        )
        ALL_SCENARIOS_MUST_HAVE_GHERKIN_CONTENT = (
            "All scenarios must have Gherkin content."
        )
        BDD_FEATURE_FILE_PATHNAME_IS_DELETED = (
            "BDD Feature file '{feature_file_pathname}' is deleted"
        )
        BDD_FEATURE_FILE_PATHNAME_IS_SAVED = (
            "BDD Feature file '{feature_file_pathname}' is saved"
        )
        DATA_WITH_PROJECT_ID_NOT_FOUND_IN_JSON_NOTHING_TO_UPDATE = (
            'Data with project ID "{project_id}" not found in JSON. Nothing to update.'
        )
        DATA_WITH_SUITE_ID_NOT_FOUND_IN_JSON_NOTHING_TO_UPDATE = (
            'Data with Suite ID "{suite_id}" not found in JSON. Nothing to update.'
        )
        EACH_SCENARIO_MUST_HAVE_A_TEST_LEVEL = "Each scenario must have a test level."
        EACH_SCENARIO_MUST_HAVE_A_TEST_APPROACH = (
            "Each scenario must have a test approach."
        )
        EACH_SCENARIO_MUST_HAVE_A_TEST_DURATION = (
            "Each scenario must have a test duration."
        )
        FEATURE_NAME_IS_REQUIRED = "Feature Name is required."
        FEATURE_FILE_WAS_NOT_FOUND = "Feature file was not found"
        DELETION_FAILED_FEATURE_FILE_NOT_FOUND = (
            "Deletion of JSON file failed. Feature file not found."
        )
        GHERKIN_FEATURE_CONTENT_IS_REQUIRED = "Gherkin Feature content is required."
        NO_DATA_FOUND_NOTHING_TO_DELETE = "No data found. Nothing to delete."
        NO_DATA_FOUND_NOTHING_TO_UPDATE = "No data found. Nothing to update."
        PLEASE_FILL_IN_THE_FIELDS_BEFORE_CHOOSING_AN_ACTION = (
            "Please, fill in the fields before choosing an action"
        )
        PROJECT_NAME_IS_REQUIRED = "Project Name is required."
        PROJECT_PROJECT_ID_IS_CREATED = "Project '{project_id}' is created"
        PROJECT_PROJECT_ID_IS_UPDATED = "Project '{project_id}' is updated"
        PROJECT_PROJECT_ID_IS_DELETED = "Project '{project_id}' is deleted"
        PROJECT_REFERENCE_IS_REQUIRED = "Project reference is required."
        SUITE_NAME_IS_REQUIRED = "Suite Name is required."
        SUITE_REFERENCE_IS_REQUIRED = "Suite reference is required."
        SUITE_SUITE_ID_IS_CREATED = "Suite '{suite_id}' is created"
        SUITE_SUITE_ID_IS_UPDATED = "Suite '{suite_id}' is updated"
        SUITE_SUITE_ID_IS_DELETED = "Suite '{suite_id}' is deleted"
        TEST_CASE_SCENARIO_IS_SAVED = "Test Case scenario '{test_id}' is saved"
        TEST_CASE_STEPS_ARE_SAVED = "Test Case Steps are saved"
        TEST_LEVEL_IS_REQUIRED = "Test Level is required."
        TEST_NAME_IS_REQUIRED = "Test Name is required."

    class FieldText:
        ADD_NEW_SCENARIO = "+ Add New Scenario"
        ADD_PRECONDITION = "+ Add Precondition"
        ADD_STEP = "+ Add Step"
        API = "API"
        BDD_SCENARIO_FORMAT = "BDD Scenario format"
        CATEGORIES_SELECTED = "Categories selected"
        CHOOSE_TEST_LEVEL_APPROACH = "Choose the test level/approach"
        CHOOSE_TEST_CATEGORY = "Choose the test category"
        COMPONENT = "Component"
        CONTRACT = "Contract"
        CRITICAL_TEST = "Critical Test"
        DELETE = "Delete"
        DELETE_FILE = "Delete File"
        DESKTOP = "Desktop"
        E2E = "E2E"
        EDGE_CASE = "Edge Case"
        EG_FEATURE_USER_LOGIN = "E.g., Feature: User Login"
        ENTER_AVERAGE_TEST_EXECUTION_DURATION = (
            "Enter the average test execution duration (HH:mm)"
        )
        ENTER_EXPECTED_RESULT = "Enter Expected Result"
        ENTER_FEATURE_NAME = "Enter Feature name"
        ENTER_PROJECT_ID_TO_DELETE = "Enter a project ID to delete"
        ENTER_PROJECT_NAME = "Enter Project name"
        ENTER_SCENARIO_LEVEL = "Enter scenario level"
        ENTER_STEP = "Enter Step"
        ENTER_SUITE_ID_TO_DELETE = "Enter a Suite ID to delete"
        ENTER_SUITE_NAME = "Enter Suite name"
        ENTER_TEST_LEVEL = "Enter test level"
        ENTER_YOUR_GHERKIN_FEATURE = "Enter your Gherkin Feature"
        ENTER_YOUR_GHERKIN_SCENARIO = "Enter your Gherkin Scenario"
        ENTER_PRECONDITION = "Enter Precondition"
        ENTER_PRECONDITIONS_FOR_THIS_TEST_CASE = (
            "Enter the Preconditions for this Test Case"
        )
        ENTER_TEST_CASE_TITLE_OR_OBJECTIVE = "Enter test case title or objective"
        ENTER_TEST_CASE_STEPS_AND_EXPECTED_RESULTS = (
            "Enter the Test Case steps and expected results"
        )
        EXPLORATORY = "Exploratory"
        FEATURE_ID = "Feature ID"
        GENERATE_NEW_ID = "Generate new ID"
        INTEGRATION = "Integration"
        MOBILE = "Mobile"
        NO_OPTIONS_SELECTED = "No options selected."
        PERFORMANCE = "Performance"
        PROJECT_ID = "Project ID"
        REQUIRED_FIELDS = "Required fields"
        REQUIREMENTS_LINK = "Requirements Link"
        SAVE = "Save"
        SAVE_FEATURE = "Save Feature"
        SAVE_NEW_TEST_CASE = "Save new Test Case"
        SCRIPTED_TEST_FORMAT = "Scripted Test format"
        SECURITY = "Security"
        SELECT_PROJECT_NAME = "Select Project name"
        SELECT_SUITE_NAME = "Select Suite name"
        SELECT_TEST_APPROACH = "Selected the test approach"
        SELECT_TEST_APPROACH_FOR_THIS_SCENARIO = (
            "Select the test approach for this scenario"
        )
        SMOKE_TEST = "Smoke Test"
        SUITE_ID = "Suite ID"
        THIS_SCENARIO_TAKES_TIME = "This scenario takes {time}"
        THIS_TEST_TAKES_TIME = "This test takes {time}"
        UNIT = "Unit"
        UPDATE = "Update"
        USABILITY = "Usability"
