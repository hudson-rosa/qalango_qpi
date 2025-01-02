import re

class StringHandler:

    def replace_last_char_occurence(base_string, char_to_replace, new_char):
        return str(base_string)[::-1].replace(char_to_replace, new_char, 1)[::-1]

    def get_id_format(base_string):
        return str(base_string).split("(")[1].rstrip(")")

    def get_name_format(base_string):
        return str(base_string).split("(")[0].strip()

    def format_time_to_hh_mm(value):
        hours = value // 60
        minutes = value % 60

        show_hours = ""
        if hours > 0:
            show_hours = f"{hours}h "
        return f"{show_hours}{minutes:02d}m"

    def remove_brackets_quotes_and_commas_from_string(base_string):
        return re.sub(r"[()\[\]{};'\",]", "", base_string)