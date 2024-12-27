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

    class ProjectDataJSON:
        PROJECT_ID = "project_id"
        PROJECT_NAME = "project_name"
        PROJECT_REF = "project_ref"

    class SuiteDataJSON:
        SUITE_ID = "suite_id"
        SUITE_NAME = "suite_name"
        SUITE_REF = "suite_ref"

    class TestEffortsDataJSON:
        PROJECT_NAME = "project_name"
        PROJECT_ID = "project_id"
        TEST_APPROACH = "test_approach"
        TEST_ID = "test_id"
        TEST_NAME = "test_name"
        TEST_LEVEL = "test_level"
        SUITE_NAME = "suite_name"
        TOTAL_TIME = "total_time"

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
