import json
import pandas as pd


class DataMapper:

    def __init__(self, filename=""):
        self.filename = filename

    def get_composed_data_frame(self):
        dataset = self.load_from_json_storage()
        return pd.DataFrame(dataset)
    
    def get_dataframe(self, datalist):
        return pd.DataFrame(datalist)

    def save_to_json_storage(self, new_data):
        with open(self.filename, "w") as f:
            json.dump(new_data, f)
            
    def load_from_json_storage(self):
        try:
            with open(self.filename, "r") as file:
                dataset = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            dataset = []
        return dataset

    def get_all_data(self):
        retrieved_data = self.load_from_json_storage()
        for row in retrieved_data:
            print(row)
        return retrieved_data

    def save_input(self, entry_data):
        dataset = self.load_from_json_storage()
        dataset.append(entry_data)
        self.save_to_json_storage(dataset)
