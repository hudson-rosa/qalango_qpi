import inspect


class TestLevel:

    level = {
        "unit": {"label": "Unit", "tier": 1, "ref": "unit"},
        "integration": {"label": "Integration", "tier": 2, "ref": "integration"},
        "component": {"label": "Component", "tier": 3, "ref": "component"},
        "contract": {"label": "Contract", "tier": 4, "ref": "contract"},
        "api": {"label": "API", "tier": 5, "ref": "api"},
        "e2e": {"label": "End-To-End", "tier": 6, "ref": "e2e"},
        "performance": {"label": "Performance", "tier": 7, "ref": "performance"},
        "security": {"label": "Security", "tier": 8, "ref": "security"},
        "usability": {"label": "Usability", "tier": 9, "ref": "usability"},
        "exploratory": {"label": "Exploratory", "tier": 10, "ref": "exploratory"},
    }

    @classmethod
    def get_option(cls, property_to_pick="", from_level=""):
        return cls.level[from_level][property_to_pick]
