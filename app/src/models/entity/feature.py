from src.utils.constants.constants import Constants

class Feature:
    def __init__(self, feature_id: str, feature_name: str):
        self.feature_id = feature_id
        self.feature_name = feature_name

    def __str__(self):
        return f"{self.feature_name} ({self.feature_id})"

    def to_dict(self):
        return {
            Constants.FeaturesDataJSON.FEATURE_ID: self.feature_id,
            Constants.FeaturesDataJSON.FEATURE_NAME: self.feature_name,
        }

    @staticmethod
    def from_dict(data: dict):
        return Feature(
            feature_id=data.get(Constants.FeaturesDataJSON.FEATURE_ID),
            feature_name=data.get(Constants.FeaturesDataJSON.FEATURE_NAME),
        )
