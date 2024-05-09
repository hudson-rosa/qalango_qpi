import sys, os
from unittest.mock import patch
from data_processing import DataProcessing
from json_data_handler import JsonDataHandler

def test_get_test_names_and_times_dictionary():
    compose_data_frame_class_attr = 'compose_data_frame'
    data_handler_mock = {
        "test1": {"test_name": "Test 1", "total_time": 10},
        "test2": {"test_name": "Test 2", "total_time": 20}
    }

    def mock_compose_data_frame():
        return data_handler_mock

    with patch.object(JsonDataHandler, compose_data_frame_class_attr, mock_compose_data_frame):
        actual = DataProcessing.get_test_names_and_times_dictionary()

    expected_result = {
        "test_name": ["Test 1", "Test 2"],
        "total_time": [10, 20]
    }

    assert actual == expected_result