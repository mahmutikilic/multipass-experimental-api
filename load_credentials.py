import json
from werkzeug.security import generate_password_hash, check_password_hash


class Users:
    def __init__(self,
                 username,
                 password):
        username=username
        password=password
        credentials = []

    def load_users(self):
        with open('config/users.json') as users_file:
            loadfile = json.load(users_file)
            return loadfile

    def set_auth(self):
        jsonfile = self.load_users()
        for user in jsonfile:
            self.credentials.append(
                {
                    "username" : user["username"],
                    "password" : generate_password_hash(user["password"])
                }
            )





@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())
