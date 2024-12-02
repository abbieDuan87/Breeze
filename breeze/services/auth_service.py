import time

from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

from breeze.utils.cli_utils import print_system_message, direct_to_dashboard, clear_screen
from breeze.utils.data_utils import load_data, save_data
from breeze.utils.constants import REGISTER_BANNER_STRING


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
                )
            case "m":
                return MHWP(username, password, first_name, last_name, email)
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

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        print('Username must be between two and ten characters, and is converted to lowercase.')
        while True:
            username = input("Username: ").strip().lower()
            if not username:
                print_system_message("Username cannot be empty. Please try again.")
                continue
            if username in self.users:
                print_system_message("Username already taken! Please choose another.")
                continue
            if len(username) < 2 or len(username) > 10:
                print_system_message("Username must be between two and ten characters! Please try again.")
                continue
            break

        password = input("Password: ").strip()
        emergency_contact_email = None
        
        if role == "p":
            emergency_contact_email = input("Emergency contact email: ").strip()

        while True:
            clear_screen()
            print(REGISTER_BANNER_STRING)
            if role == 'p':
                print_system_message(
                    f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                    f"Username: {username}\nPassword: {password}\nEmergency Contact Email: {emergency_contact_email}"
                )
            else: 
                print_system_message(
                    f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                    f"Username: {username}\nPassword: {password}"
                )
            print("Would you like to edit any of the information? Enter [E] to edit, or type any other key to confirm details.")
            response = input("> ").strip().lower()
            if response == 'e':
                clear_screen()
                print(REGISTER_BANNER_STRING)
                if role == 'p':
                    print_system_message(
                        f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                        f"Username: {username}\nPassword: {password}\nEmergency Contact Email: {emergency_contact_email}"
                    )
                    print('Enter the value of the data you wish to edit (1-6), or type any other key to confirm:')
                
                else: 
                    print_system_message(
                        f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                        f"Username: {username}\nPassword: {password}"
                    )
                    print('Enter the value of the data you wish to edit (1-5), or type any other key to confirm:')
                
                print('[1] First Name\n[2] Last Name\n[3] Email\n[4] Username\n[5] Password')
                if role == 'p':
                    print('[6] Emergency Contact Email')
                to_edit = input('> ').strip().lower()
                match to_edit:
                    case '1':
                        first_name = input("First name: ").strip()
                    case '2':
                        last_name = input("Last name: ").strip()
                    case '3':
                        email = input("Email: ").strip()
                    case '4':
                        print('Username must be between two and ten characters, and is converted to lowercase.')
                        while True:
                            username = input("Username: ").strip().lower()
                            if not username:
                                print_system_message("Username cannot be empty. Please try again.")
                                continue
                            if username in self.users:
                                print_system_message("Username already taken! Please choose another.")
                                continue 
                            if len(username) < 2 or len(username) > 10:
                                print_system_message("Username must be between two and ten characters! Please try again.")
                                continue
                            break
                    case '5':
                        password = input("Password: ").strip()
                    case '6':
                        if role == 'p':
                            emergency_contact_email = input ("Emergency Contact Email: ").strip()
                        else:
                            break
                    case _:
                        break
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
        )
        if role == "p" and new_user:
            mhwp = self.find_mhwp_with_fewest_patients()
            if mhwp:
                mhwp.add_patient(new_user.get_username())
                new_user.set_assigned_mhwp(mhwp.get_username())
                print_system_message(f"You have been assigned to MHWP: {mhwp.get_first_name()} {mhwp.get_last_name()}.")

        if new_user:
            self.users[new_user.get_username()] = new_user
            self.save_data_to_file()
            direct_to_dashboard("Account created successfully!")
    
    def find_mhwp_with_fewest_patients(self):
        """Finds the MHWP with the fewest assigned patients.

        Returns:
            MHWP: The MHWP with the fewest assigned patients, or None.
        """
        mhwps = []
        for user in self.users.values():
            if isinstance(user, MHWP):
                mhwps.append(user)

        if mhwps:
            # Find MHWP with the fewest assigned patients
            return min(mhwps, key=lambda mhwp: len(mhwp.get_assigned_patients()))
        else:
            return None


    def get_all_users(self):
        return self.users

    def get_user_by_username(self, username):
        return self.users.get(username, None)
