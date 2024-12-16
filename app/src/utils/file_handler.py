import os


class FileHandler:
    """Enter parameter 'file_pathname' like this/is/my/path/useful_file.json"""

    def delete_file(file_pathname):
        try:
            os.remove(file_pathname)
            print(f"File {file_pathname} has been deleted.")
        except FileNotFoundError:
            print(f"File {file_pathname} does not exist.")
        except PermissionError:
            print(f"Permission denied to delete {file_pathname}.")
        except Exception as e:
            print(f"An error occurred deleting file: {e}")

    def save_new_file(file_pathname, content=""):
        try:
            with open(str(file_pathname), "w", encoding="utf-8") as file:
                file.write(content)
            return f"File '{file_pathname}' has been saved successfully!"
        except Exception as e:
            return f"Error saving file: {e}"

    def count_string_occurrencies_in_file(file_pathname, string_to_count=""):
        try:
            with open(str(file_pathname), "r", encoding="utf-8") as file:
                content = file.read()
            count = content.count(string_to_count)
            return count
        except FileNotFoundError:
            return f"Error: File '{file_pathname}' not found."
        except Exception as e:
            return f"An error occurred reading file: {e}"
