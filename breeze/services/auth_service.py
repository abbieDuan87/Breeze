import time
from datetime import date

from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

from breeze.utils.cli_utils import print_system_message, direct_to_dashboard
from breeze.utils.data_utils import load_data, save_data


class AuthService:
    def __init__(self):
        users_data, _ = load_data("./data/users.json")
        self.users = {user.get_username(): user for user in users_data.values()}
        self.current_user = None

    def save_data_to_file(self):
        """Save the updated user data to the JSON file"""
        save_data("./data/users.json", list(self.users.values()))

    def login(self):
        while True:
            username = input("Username: ").strip()
            if not username:
                print_system_message("Username cannot be empty. Please try again.")
                continue
            break
        password = input("Password: ")
        user = self.users.get(username)
        if user and user.login(password):
            print(f"Welcome, {username}")
            time.sleep(1)
            self.current_user = user
            return user
        return None

    def logout(self):
        if self.current_user:
            self.current_user = None
            return None

    def _register_role(
        self,
        role,
        username,
        password,
        first_name,
        last_name,
        email,
        emergency_contact_email,
        date_of_birth,
        gender
    ):
        """Helper method to create a new user based on role.
        Args:
            role (str)
            username (str)
            password (str)
            first_name (str)
            last_name (str)
            email (str)
            emergency_contact_email (str, optional)
        """
        match role.strip().lower():
            case "a":
                return Admin(username, password, first_name, last_name, email)
            case "p":
                return Patient(
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    emergency_contact_email,
                    date_of_birth,
                    gender
                )
            case "m":
                return MHWP(username, password, first_name, last_name, email, date_of_birth, gender)
            case _:
                print_system_message("Invalid role! Please select a valid option.")
                return None

    def register(self):
        """A function to register new user

        Returns:
            user (Admin/Patient/MHWP): The created new user
        """
        print("Please choose a role:\n\n[P]atient\n[M]HWP\n")

        while True:
            role = input("Select a role [P/M]: ").strip().lower()
            if role in ["p", "m"]:
                break
            else:
                print_system_message("Invalid role. Please select a valid option.")

        # Gets DOB // Checks it's valid // If role is patient checks if they are 16
        while True:
            date_of_birth = input("Date of birth (DD/MM/YYYY): ").strip()
            try:
                temp_date = date(int(date_of_birth.split("/")[2]), int(date_of_birth.split("/")[1]), int(date_of_birth.split("/")[0]))
            except:
                print("Invalid date")
            if role == "p":
                if date.today().year - temp_date.year - ((date.today().month, date.today().day) < (temp_date.month, temp_date.day))>= 16:
                    break
                else:
                    direct_to_dashboard("You are not old enough to register with Breeze") 
                    return False
                    break
            else:
                break

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()

        while True:
            email = input("Email: ").strip()
            if '@' and '.' not in email:
                print("Invalid email")
            else:
                break

        while True:
            gender = input("Enter your gender (M/F/O): ").strip().lower()
            if gender not in ["m", "f", "o"]:
                print("Please enter a valid option")
            else:
                break

        while True:
            username = input("Username: ").strip()
            if not username:
                print_system_message("Username cannot be empty. Please try again.")
                continue
            if username in self.users:
                print_system_message("Username already taken! Please choose another.")
                continue
            break

        password = input("Password: ").strip()
        emergency_contact_email = None
        if role == "p":
            while True:
                emergency_contact_email = input("Emergency contact email: ").strip()
                if '@' and '.' not in emergency_contact_email:
                    print("Invalid email")
                else:
                    break
                
        new_user = self._register_role(
            role,
            username,
            password,
            first_name,
            last_name,
            email,
            emergency_contact_email,
            date_of_birth,
            gender
        )
        if new_user:
            self.users[new_user.get_username()] = new_user
            self.save_data_to_file()
            direct_to_dashboard("Account created successfully!")

    def get_all_users(self):
        return self.users

    def get_user_by_username(self, username):
        return self.users.get(username, None)
