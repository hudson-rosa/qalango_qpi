import html
import dash
from dash import html
from behave.parser import ParserError, parse_feature
from src.utils.constants.constants import Constants

validation_error_classname = "validation-error"
validation_success_classname = "validation-success"


class ValidationUtils:

    def identify_triggering_action(callback_context=dash.callback_context):
        return (
            None
            if not callback_context.triggered
            else str(callback_context.triggered[0]["prop_id"]).split(".")[0]
        )

    def identify_triggering_action_on_nested_dict(
        callback_context=dash.callback_context,
    ):
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
            error_message = (
                f"{Constants.Messages.MISSING_FIELDS}:\n   ‣ " + "\n   ‣ ".join(errors)
            )
            return False, html.Pre(error_message, className=validation_error_classname)

        return True, html.Pre(
            "✅ " + str(feature_action),
            className=validation_success_classname,
        )

    def validate_gherkin_syntax(gherkin_content=""):
        try:
            parse_feature(gherkin_content)
            return Constants.Messages.SYNTAX_IS_VALID, validation_success_classname
        except ParserError as pe:
            return (
                f"{Constants.Messages.SYNTAX_ERROR}: \n{str(pe)}",
                validation_error_classname,
            )
        except Exception as ex:
            return (
                f"{Constants.Messages.UNEXPECTED_ERROR}: \n{str(ex)}",
                validation_error_classname,
            )
