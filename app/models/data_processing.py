import json
import pandas as pd
import app.controllers.app_path_config as app_path_config
from app.utils.json_data_handler import JsonDataHandler

data_path = app_path_config.get_data_storage_path()


class DataProcessing(JsonDataHandler):

    @staticmethod
    def get_test_names_and_times_dictionary():
        test_names = []
        total_times = []
        data_handler = JsonDataHandler(data_path).compose_data_frame()

        for key, value in data_handler.items():
            test_name = value.get("test_name")
            total_time = value.get("total_time")

            if test_name is not None:
                test_names.append(test_name)
            if total_time is not None:
                total_times.append(total_time)

        print("Test Names:", test_names)
        print("Total Times:", total_times)
        return {"test_name": test_names, "total_time": total_times}
