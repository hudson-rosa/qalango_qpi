import unittest
from unittest.mock import MagicMock, patch
from app.src.models.data_processing import DataProcessing

patch_data_processing_fn_compose_data_frame = (
    "src.models.data_processing.JsonDataHandler.compose_data_frame"
)


class TestDataProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_processing = DataProcessing()

    def test_get_test_names_and_times_dictionary(self):
        expected_result = {
            "test_name": [
                "Test 0",
                "Test 1",
                "Test 2",
                "Test 3",
            ],
            "total_time": [0.0, 10, 20, 1000000],
        }

        with patch(
            patch_data_processing_fn_compose_data_frame
        ) as mock_compose_data_frame:
            mock_compose_data_frame.return_value = {
                1: {"test_name": "Test 0", "total_time": 0.0},
                2: {"test_name": "Test 1", "total_time": 10},
                3: {"test_name": "Test 2", "total_time": 20},
                4: {"test_name": "Test 3", "total_time": 1000000},
            }
            result = DataProcessing.get_test_names_and_times_dictionary()

        self.assertEqual(result, expected_result)

    def test_get_test_names_and_times_empty_data(self):
        with patch(
            patch_data_processing_fn_compose_data_frame
        ) as mock_compose_data_frame:
            mock_compose_data_frame.return_value = {}
            result = DataProcessing.get_test_names_and_times_dictionary()
        self.assertEqual(result, {"test_name": [], "total_time": []})

    def test_get_test_names_and_times_missing_data(self):
        with patch(
            patch_data_processing_fn_compose_data_frame
        ) as mock_compose_data_frame:
            mock_compose_data_frame.return_value = {
                1: {"test_name": "Test 0", "total_time": 0.0},
                2: {"test_name": "Test 1"},  # Missing total_time
            }
            result = DataProcessing.get_test_names_and_times_dictionary()
        self.assertEqual(result, {"test_name": ["Test 0"], "total_time": [0.0]})


if __name__ == "__main__":
    unittest.main()
