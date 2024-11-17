from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

from breeze.utils.cli_utils import print_system_message
from breeze.utils.data_utils import load_data, save_data

class AuthService:
    def __init__(self):
        self.users = {user.get_username(): user for user in load_data("./data/users.json").get("users", [])}
        self.current_user = None
    
    def save_data_to_file(self):
        """Save the updated user data to the JSON file"""
        data = {"users": [user.to_dict() for user in self.users.values()]}
        save_data("./data/users.json", data)

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        user = self.users.get(username)
        if user and user.login(password):
            print(f"Welcome, {username}")
            self.current_user = user
            return user
        return None
    
    def logout(self):
        if self.current_user:
            self.current_user = None
            return None
    
    def _register_role(self, role, username, password, first_name, last_name, email, emergency_contact_email):   
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
                return Admin(username, password, first_name,last_name, email)
            case "p":
                return Patient(username, password,first_name, last_name, email, emergency_contact_email)
            case "m":
                return MHWP(username, password,first_name,last_name, email)
            case _:
                print_system_message("Invalid role! Please select a valid option.")
                return None

    def register(self):
        """A function to register new user

        Returns:
            user (Admin/Patient/MHWP): The created new user
        """
        print("Please choose a role:\n[A]dmin\n[P]atient\n[M]HWP")
        while True:
            role = input("Select a role [A/P/M]: ").strip().lower()
            if role in ["a", "p", "m"]:
                break
            else:
                print_system_message("Invalid role. Please select a valid option.")

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        username = input("Username: ").strip()
        
        # Check if username already exists
        if username in self.users:
            print_system_message("Username already taken! Please choose another.")
            return None
        
        password = input("Password: ").strip()
        emergency_contact_email = None
        if role =="p":
            emergency_contact_email = input("Emergency contact email: ").strip()

            # Register role based on input
        new_user = self._register_role(role, username, password, first_name, last_name, email, emergency_contact_email)
        if new_user:
            self.users[new_user.get_username()] = new_user
            print_system_message("Account created successfully! Press B to go back and log in.")
            self.save_data_to_file()
            
        return new_user

    def get_all_users(self):
        return self.users