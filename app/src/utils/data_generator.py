from datetime import datetime, timedelta


class DataGenerator:

    def __init__(self, filename="app/data/storage/test_data.json"):
        self.filename = filename

    def generate_random_date(self, today=datetime.now(), random_days=0):
        random_date = today + timedelta(days=int(random_days))
        return random_date.strftime("%Y-%m-%d")
