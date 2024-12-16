import inspect
from src.utils.constants.constants import Constants


class TestLevel:

    level = {
        Constants.TestLevelsEntity.UNIT: {
            "label": "Unit",
            "tier": 1,
            "ref": Constants.TestLevelsEntity.UNIT,
        },
        Constants.TestLevelsEntity.INTEGRATION: {
            "label": "Integration",
            "tier": 2,
            "ref": Constants.TestLevelsEntity.INTEGRATION,
        },
        Constants.TestLevelsEntity.COMPONENT: {
            "label": "Component",
            "tier": 3,
            "ref": Constants.TestLevelsEntity.COMPONENT,
        },
        Constants.TestLevelsEntity.CONTRACT: {
            "label": "Contract",
            "tier": 4,
            "ref": Constants.TestLevelsEntity.CONTRACT,
        },
        Constants.TestLevelsEntity.API: {
            "label": "API",
            "tier": 5,
            "ref": Constants.TestLevelsEntity.API,
        },
        Constants.TestLevelsEntity.E2E: {
            "label": "End-To-End",
            "tier": 6,
            "ref": Constants.TestLevelsEntity.E2E,
        },
        Constants.TestLevelsEntity.PERFORMANCE: {
            "label": "Performance",
            "tier": 7,
            "ref": Constants.TestLevelsEntity.PERFORMANCE,
        },
        Constants.TestLevelsEntity.SECURITY: {
            "label": "Security",
            "tier": 8,
            "ref": Constants.TestLevelsEntity.SECURITY,
        },
        Constants.TestLevelsEntity.USABILITY: {
            "label": "Usability",
            "tier": 9,
            "ref": Constants.TestLevelsEntity.USABILITY,
        },
        Constants.TestLevelsEntity.EXPLORATORY: {
            "label": "Exploratory",
            "tier": 10,
            "ref": Constants.TestLevelsEntity.EXPLORATORY,
        },
    }

    @classmethod
    def get_option(cls, property_to_pick="", from_level=""):
        return cls.level[from_level][property_to_pick]
