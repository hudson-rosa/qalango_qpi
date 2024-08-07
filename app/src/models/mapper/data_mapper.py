import json
import pandas as pd
import random
from datetime import datetime, timedelta
import src.controllers.app_path_config as app_path_config


class DataMapper:

    def __init__(self, filename=""):
        self.json_storage = (
            filename == "" if app_path_config.get_data_storage_path() else filename
        )
        self.filename = filename

    def compose_data_frame(self):
        dataset = self.load_from_json_storage()
        return pd.DataFrame(dataset)
    
    def get_dataframe(self, datalist):
        return pd.DataFrame(datalist)

    def save_to_json_storage(self, data):
        with open(self.json_storage, "w") as f:
            json.dump(data, f)
            
    def load_from_json_storage(self):
        try:
            with open(self.filename, "r") as file:
                dataset = json.load(file)
        except FileNotFoundError:
            dataset = []
        return dataset

    def get_all_storage_data(self):
        retrieved_data = self.load_from_json_storage()
        for row in retrieved_data:
            print(row)
        return retrieved_data

    def add_into_storage(self, entry_data):
        dataset = self.load_from_json_storage()
        dataset.append(entry_data)
        self.save_to_json_storage(dataset)
