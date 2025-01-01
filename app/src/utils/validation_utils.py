import html
from dash import html


class ValidationUtils:

    def validate_mandatory_field_rules(
        feature_action="Form is saved", validation_rules=[]
    ):
        errors = []
        errors.extend(message for condition, message in validation_rules if condition)

        if errors:
            error_message = "⚠️ Missing Fields:\n   ‣ " + "\n   ‣ ".join(errors)
            return False, html.Pre(error_message, className="validation-error")

        return True, html.Pre(
            "✅ " + str(feature_action) + " successfully",
            className="validation-success",
        )
