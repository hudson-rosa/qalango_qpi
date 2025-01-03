from src.utils.constants.constants import Constants


class TestCategory:

    category = {
        Constants.TestCategoriesEntity.CRITICAL_TEST: {
            "label": Constants.FieldText.CRITICAL_TEST,
            "ref": Constants.TestCategoriesEntity.CRITICAL_TEST,
        },
        Constants.TestCategoriesEntity.EDGE_CASE: {
            "label": Constants.FieldText.EDGE_CASE,
            "ref": Constants.TestCategoriesEntity.EDGE_CASE,
        },
        Constants.TestCategoriesEntity.SMOKE_TEST: {
            "label": Constants.FieldText.SMOKE_TEST,
            "ref": Constants.TestCategoriesEntity.SMOKE_TEST,
        },
        Constants.TestCategoriesEntity.MOBILE: {
            "label": Constants.FieldText.MOBILE,
            "ref": Constants.TestCategoriesEntity.MOBILE,
        },
        Constants.TestCategoriesEntity.DESKTOP: {
            "label": Constants.FieldText.DESKTOP,
            "ref": Constants.TestCategoriesEntity.DESKTOP,
        },
    }

    @classmethod
    def get_option(cls, property_to_pick="", from_type=""):
        return cls.category[from_type][property_to_pick]
