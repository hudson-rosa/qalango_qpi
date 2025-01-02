from src.utils.constants.constants import Constants


class TestLevel:

    level = {
        Constants.TestLevelsEntity.UNIT: {
            "label": Constants.FieldText.UNIT,
            "tier": 1,
            "ref": Constants.TestLevelsEntity.UNIT,
        },
        Constants.TestLevelsEntity.INTEGRATION: {
            "label": Constants.FieldText.INTEGRATION,
            "tier": 2,
            "ref": Constants.TestLevelsEntity.INTEGRATION,
        },
        Constants.TestLevelsEntity.COMPONENT: {
            "label": Constants.FieldText.COMPONENT,
            "tier": 3,
            "ref": Constants.TestLevelsEntity.COMPONENT,
        },
        Constants.TestLevelsEntity.CONTRACT: {
            "label": Constants.FieldText.CONTRACT,
            "tier": 4,
            "ref": Constants.TestLevelsEntity.CONTRACT,
        },
        Constants.TestLevelsEntity.API: {
            "label": Constants.FieldText.API,
            "tier": 5,
            "ref": Constants.TestLevelsEntity.API,
        },
        Constants.TestLevelsEntity.E2E: {
            "label": Constants.FieldText.E2E,
            "tier": 6,
            "ref": Constants.TestLevelsEntity.E2E,
        },
        Constants.TestLevelsEntity.PERFORMANCE: {
            "label": Constants.FieldText.PERFORMANCE,
            "tier": 7,
            "ref": Constants.TestLevelsEntity.PERFORMANCE,
        },
        Constants.TestLevelsEntity.SECURITY: {
            "label": Constants.FieldText.SECURITY,
            "tier": 8,
            "ref": Constants.TestLevelsEntity.SECURITY,
        },
        Constants.TestLevelsEntity.USABILITY: {
            "label": Constants.FieldText.USABILITY,
            "tier": 9,
            "ref": Constants.TestLevelsEntity.USABILITY,
        },
        Constants.TestLevelsEntity.EXPLORATORY: {
            "label": Constants.FieldText.EXPLORATORY,
            "tier": 10,
            "ref": Constants.TestLevelsEntity.EXPLORATORY,
        },
    }

    @classmethod
    def get_option(cls, property_to_pick="", from_level=""):
        return cls.level[from_level][property_to_pick]
