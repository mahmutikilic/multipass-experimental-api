import json
from werkzeug.security import generate_password_hash


class Users:
    def __init__(self, path="config/users.json"):
        with open(path, "r", encoding="utf-8") as fh:
            self.users = json.load(fh)

    def credentials(self):
        creds = {}
        for user in self.users:
            creds[user["username"]] = generate_password_hash(user["password"])
        return creds
