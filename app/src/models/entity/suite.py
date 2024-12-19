from src.utils.constants.constants import Constants


class Suite:
    def __init__(self, suite_id: str, suite_name: str):
        self.suite_id = suite_id
        self.suite_name = suite_name

    def __str__(self):
        return f"{self.suite_name} ({self.suite_id})"

    def to_dict(self):
        return {
            Constants.SuiteDataJSON.SUITE_ID: self.suite_id,
            Constants.SuiteDataJSON.SUITE_NAME: self.suite_name,
        }

    @staticmethod
    def from_dict(data: dict):
        return Suite(
            suite_id=data.get(Constants.SuiteDataJSON.SUITE_ID),
            suite_name=data.get(Constants.SuiteDataJSON.SUITE_NAME),
        )
