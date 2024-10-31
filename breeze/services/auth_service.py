from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

class AuthService:
    def __init__(self):

        self.users = {
            "admin": Admin("admin", ""),
            "patient1": Patient("patient1", ""),
            "mhwp1": MHWP("mhwp1", "")
        }

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        user = self.users.get(username)
        if user and user.login(password):
            print(f"Welcome, {username}")
            return user
        return None