from datetime import datetime, timedelta
import random
import string
import hashlib
import time
import uuid


class DataGenerator:

    def __init__(self, filename="app/data/storage/test_efforts_data.json"):
        self.filename = filename

    @staticmethod
    def generate_random_date(today=datetime.now(), random_days=0):
        random_date = today + timedelta(days=int(random_days))
        return random_date.strftime("%Y-%m-%d")

    @staticmethod
    def generate_random_ascii_id(length_threshold=8):
        random_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=length_threshold)
        )
        return str(random_id).lower()

    @staticmethod
    def generate_encrypted_data(entry_data):
        sha256_hash_object = hashlib.sha256(entry_data.encode())
        encrypted_id = sha256_hash_object.hexdigest()
        return str(encrypted_id).lower()

    @staticmethod
    def generate_uuid():
        new_uuid = str(uuid.uuid4())
        return str(new_uuid.replace("-", "")).lower()

    @staticmethod
    def generate_aggregated_uuid(
        entry_data=str(int(time.time() * 1000)), length_threshold=10
    ):
        random_id = DataGenerator.generate_uuid() + str(
            DataGenerator.generate_encrypted_data(entry_data)
        )
        return str(random_id[:length_threshold]).lower()

    @staticmethod
    def truncate_longer_name(string_to_truncate, max_char_length_to_strict=20):
        truncated_chars_length = int(max_char_length_to_strict / 2)
        if len(string_to_truncate) > max_char_length_to_strict:
            return f"{string_to_truncate[:truncated_chars_length]}...{string_to_truncate[-truncated_chars_length:]}"
        return string_to_truncate
