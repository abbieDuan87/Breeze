from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

class AuthService:
    def __init__(self):

        self.users = {
            "admin": Admin("admin", "1234567"),
            "patient1": Patient("patient1", "1234567"),
            "mhwp1": MHWP("mhwp1", "1234567")
        }

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        user = self.users.get(username)
        if user and user.login(password):
            print(f"Welcome, {username}")
            return user
        return None