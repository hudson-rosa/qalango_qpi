import os


class ValidationUtils:

    def validate_mandatory_fields(**fields):
        """
        Validates that all provided fields have values.

        Parameters:
            fields (dict): A dictionary where keys are field names and values are the corresponding input values.

        Returns:
            tuple: (bool, str) - A tuple with a boolean indicating success and a message detailing missing fields.
        """
        missing_fields = [name.replace('_',' ').capitalize() for name, value in fields.items() if not value]

        if missing_fields:
            return (
                False,
                f"Missing mandatory fields: {', '.join(missing_fields)}",
            )
        return True, None
