
import json
import os

class Bank:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump({}, f)

    def load(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_balance(self, user_id):
        data = self.load()
        return data.get(str(user_id), 1000)

    def update_balance(self, user_id, amount):
        data = self.load()
        user_id = str(user_id)
        data[user_id] = data.get(user_id, 1000) + amount
        self.save(data)
        return data[user_id]
