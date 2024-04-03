from datetime import datetime, timedelta
import json
import pandas as pd
import random


class DataHandler:
    def __init__(self, filename="data/storage/test_data.json"):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                dataset = json.load(file)
        except FileNotFoundError:
            dataset = []
        return dataset

    def save_data(self, dataset):
        with open(self.filename, "w") as file:
            json.dump(dataset, file)

    def get_all_storage_data(self):
        retrieved_data = self.load_data()
        for row in retrieved_data:
            print(row)
        return retrieved_data

    def compose_data_frame(self):
        dataset = self.load_data()
        return pd.DataFrame(dataset)

    def add_into_storage(self, entry_data):
        dataset = self.load_data()
        dataset.append(entry_data)
        self.save_data(dataset)

    def add_test_info(self):
        max_random_data = 20
        for i in range(max_random_data):
            data_handler.add_into_storage(
                {
                    "test_name": f"Test {i+1}",
                    "test_date": self.generate_random_date(random_days=i),
                    "score": random.randint(10, 100),
                }
            )
        data_handler.get_all_storage_data()

    def generate_random_date(self, today=datetime.now(), random_days=0):
        random_date = today + timedelta(days=int(random_days))
        return random_date.strftime("%Y-%m-%d")


"""
    Run this file to generate testing data
"""
if __name__ == "__main__":
    data_handler = DataHandler()
    data_handler.add_test_info()
