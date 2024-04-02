from datetime import datetime, timedelta
import json
import pandas as pd
import random

# # Function to load data from JSON file
# def load_data():
#     try:
#         with open("test_data.json", "r") as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         data = []
#     return data


# # Function to save data to JSON file
# def save_data(data):
#     with open("test_data.json", "w") as file:
#         json.dump(data, file)


# # Function to add new test information
# def add_test_info(test_info):
#     data = load_data()
#     data.append(test_info)
#     save_data(data)

# def compose_data_frame():
#     data = load_data()
#     return pd.DataFrame(data)

# # Function to retrieve all test information
# def get_all_test_info():
#     return load_data()


# # Example usage
# if __name__ == "__main__":
#     add_test_info({"test_name": "Test 1", "test_date": "2024-02-18", "score": 85})
#     add_test_info({"test_name": "Test 2", "test_date": "2024-02-19", "score": 90})
#     add_test_info({"test_name": "Test 3", "test_date": "2024-03-25", "score": 99})

#     test_data = get_all_test_info()
#     for test in test_data:
#         print(test)


class DataHandler:
    def __init__(self, filename="test_data.json"):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save_data(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def get_all_storage_data(self):
        retrieved_data = self.load_data()
        for row in retrieved_data:
            print(row)
        return retrieved_data

    def compose_data_frame(self):
        data = self.load_data()
        return pd.DataFrame(data)

    def add_into_storage(self, entry_data):
        data = self.load_data()
        data.append(entry_data)
        self.save_data(data)

    def add_test_info(self):
        for i in range(5):
            data_handler.add_into_storage(
                {
                    "test_name": f"Test {i+1}",
                    "test_date": self.generate_random_date(),
                    "score": random.randint(10, 100),
                }
            )
        data_handler.get_all_storage_data()

    def generate_random_date(self):
        today = datetime.now()
        random_date = today + timedelta(days=random.randint(-3, 3))
        return random_date.strftime("%Y-%m-%d")

"""
    Run this file to generate testing data
"""
if __name__ == "__main__":
    data_handler = DataHandler()
    data_handler.add_test_info()
