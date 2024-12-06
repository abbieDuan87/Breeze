import time

from breeze.models.admin import Admin
from breeze.models.patient import Patient
from breeze.models.mhwp import MHWP

from breeze.utils.cli_utils import (
    print_system_message,
    direct_to_dashboard,
    clear_screen,
    is_invalid_username,
    is_invalid_date,
    is_invalid_email,
    is_valid_name,
    is_empty,
)
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
            print_system_message(f"Welcome, {username}")
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
        gender=None,
        date_of_birth=None,
        emergency_contact_email=None,
    ):
        """Helper method to create a new user based on role.
        Args:
            role (str)
            username (str)
            password (str)
            first_name (str)
            last_name (str)
            email (str)
            gender (str, optional)
            date_of_birth (str, optional)
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
                    gender=gender,
                    date_of_birth=date_of_birth,
                    emergency_contact_email=emergency_contact_email,
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

        while True:
            first_name = input("First name: ").strip()
            if is_empty(first_name):
                continue
            elif is_valid_name(first_name):
                break

        while True:
            last_name = input("Last name: ").strip()
            if is_empty(last_name):
                continue
            elif is_valid_name(last_name):
                break

        while True:
            email = input("Email: ").strip()
            if is_empty(email):
                continue
            if is_invalid_email(email):
                continue
            break

        while True:
            username = input("Username: ").strip().lower()
            if is_invalid_username(username, self.users):
                continue
            break

        password = input("Password: ").strip()

        gender = None
        date_of_birth = None
        emergency_contact_email = None

        if role == "p":
            print(
                "Gender Options:\n[M] Male\n[F] Female\n[N] Non-binary\n[T] Transgender\n[O] Other"
            )
            gender_dict = {
                "m": "Male",
                "f": "Female",
                "n": "Non-binary",
                "t": "Transgender",
                "o": "Other",
            }
            while True:
                gender = input("> ").strip().lower()
                if gender not in gender_dict.keys():
                    print_system_message("Please select a valid option.")
                else:
                    gender = gender_dict[gender]
                    break

            while True:
                date_of_birth = input("Date of Birth (DD-MM-YYYY): ")
                if is_invalid_date(date_of_birth):
                    continue
                break

            while True:
                emergency_contact_email = input(
                    "Emergency contact email (optional): "
                ).strip()
                if emergency_contact_email and is_invalid_email(
                    emergency_contact_email
                ):
                    continue
                break

        while True:
            clear_screen()
            print(REGISTER_BANNER_STRING)
            if role == "p":
                print_system_message(
                    f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                    f"Username: {username}\nPassword: {password}\nGender: {gender}\n"
                    f"Date of Birth: {date_of_birth}\nEmergency Contact Email: {emergency_contact_email}"
                )
            else:
                print_system_message(
                    f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                    f"Username: {username}\nPassword: {password}"
                )
            print(
                "Would you like to edit any of the information? Enter [E] to edit, or type any other key to confirm details."
            )
            response = input("> ").strip().lower()
            if response == "e":
                clear_screen()
                print(REGISTER_BANNER_STRING)
                if role == "p":
                    print_system_message(
                        f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                        f"Username: {username}\nPassword: {password}\nEmergency Contact Email: {emergency_contact_email}"
                    )
                    print(
                        "Enter the value of the data you wish to edit (1-8), or type any other key to confirm:"
                    )

                else:
                    print_system_message(
                        f"First name: {first_name}\nLast name: {last_name}\nEmail: {email}\n"
                        f"Username: {username}\nPassword: {password}"
                    )
                    print(
                        "Enter the value of the data you wish to edit (1-5), or type any other key to confirm:"
                    )

                print(
                    "[1] First Name\n[2] Last Name\n[3] Email\n[4] Username\n[5] Password"
                )
                if role == "p":
                    print("[6] Gender\n[7] Date of Birth\n[8] Emergency Contact Email")

                to_edit = input("> ").strip().lower()

                if role == "p":
                    match to_edit:
                        case "6":
                            while True:
                                gender = input("> ").strip().lower()
                                if gender not in gender_dict.keys():
                                    print_system_message(
                                        "Please select a valid option."
                                    )
                                else:
                                    gender = gender_dict[gender]
                                    break
                        case "7":
                            while True:
                                date_of_birth = input("Date of Birth (DD/MM/YYYY): ")
                                if is_invalid_date(date_of_birth):
                                    continue
                                break
                        case "8":
                            while True:
                                emergency_contact_email = input(
                                    "Emergency Contact Email (Optional): "
                                ).strip()
                                if emergency_contact_email and is_invalid_email(
                                    emergency_contact_email
                                ):
                                    continue
                                break
                        case _:
                            pass
                match to_edit:
                    case "1":
                        while True:
                            first_name = input("First name: ").strip()
                            if is_empty(first_name):
                                continue
                            elif is_valid_name(first_name):
                                break
                    case "2":
                        while True:
                            last_name = input("Last name: ").strip()
                            if is_empty(last_name):
                                continue
                            elif is_valid_name(last_name):
                                break
                    case "3":
                        while True:
                            email = input("Email: ").strip()
                            if is_invalid_email(email):
                                continue
                            break
                    case "4":
                        while True:
                            username = input("Username: ").strip().lower()
                            if is_invalid_username(username, self.users):
                                continue
                            break
                    case "5":
                        password = input("Password: ").strip()
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
            gender,
            date_of_birth,
            emergency_contact_email,
        )
        if role == "p" and new_user:
            mhwp = self.find_mhwp_with_fewest_patients()
            if mhwp:
                mhwp.add_patient(new_user.get_username())
                new_user.set_assigned_mhwp(mhwp.get_username())
                print_system_message(
                    f"You have been assigned to MHWP: {mhwp.get_first_name()} {mhwp.get_last_name()}."
                )

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


if __name__ == "__main__":
    auth_servce = AuthService()
    gp1 = auth_servce.get_user_by_username("mhwp1")
    print(gp1)
    print(gp1.get_appointments())
    gp1.display_calendar()
    gp1.display_calendar(is_MHWP_view=False)
