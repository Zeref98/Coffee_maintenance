# data_manager.py
import json
import os
from config import DATA_FILE

class DataManager:
    @staticmethod
    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"machines": []}

    @staticmethod
    def save_data(data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
