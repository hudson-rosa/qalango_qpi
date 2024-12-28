class StringHandler:

    def replace_last_char_occurence(base_string, char_to_replace, new_char):
        return str(base_string)[::-1].replace(char_to_replace, new_char, 1)[::-1]

    def get_id_format(base_string):
        return str(base_string).split("(")[1].rstrip(")")

    def get_name_format(base_string):
        return str(base_string).split("(")[0].strip()
