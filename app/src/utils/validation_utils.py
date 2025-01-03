import html
import dash
from dash import html


class ValidationUtils:

    def identify_triggering_action(callback_context=dash.callback_context):
        return (
            None
            if not callback_context.triggered
            else str(callback_context.triggered[0]["prop_id"]).split(".")[0]
        )

    def identify_triggering_action_on_nested_dict(callback_context=dash.callback_context):       
        if not callback_context.triggered:
            return None
        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        return eval(triggered_id) if "{" in triggered_id else triggered_id

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
