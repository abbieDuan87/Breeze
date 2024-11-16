from breeze.utils.cli_utils import print_system_message, clear_screen, direct_to_dashboard
from breeze.utils.constants import ADMIN_BANNER_STRING
from breeze.utils.data_utils import load_data, save_data, decode_user
from breeze.models.user import User
from breeze.models.patient import Patient
from breeze.models.admin import Admin
from breeze.models.mhwp import MHWP


class AdminService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.data_file_path = './data/users.json'
    
    def show_admin_dashboard(self, user):
        """
        Displays the admin dashboard and processes user actions.

        Args:
            user (User): _The logged-in user
            
        Returns:
            bool: True if the user chose to log out, otherwise False
        """

        print(ADMIN_BANNER_STRING)
        print('Hi', user.get_username(), '!')
        print('What do you want to do today?')

        
        print('[A] Allocate patient to MHWP')
        print('[E] Edit user information')
        print('[R] Delete a user')
        print('[D] Disable a user')
        print('[V] View summary')
        print('[X] Log out')

        user_input = input("> ").strip().lower()
        match user_input:
            case "a":
                self.allocate_patient_to_mhwp()
            case "e":
                self.edit_user_information()
            case "r":
                self.delete_user()
            case "d":
                self.disable_user()
            case "v":
                self.view_summary()
            case "x":
                return True
            case _:
                print_system_message("Invalid choice. Please try again.")

        return False

    def allocate_patient_to_mhwp(self):
        pass

    def edit_user_information(self):
        """
        Allows admin to edit information for a patient or an MWHP
        """
        print_system_message("Edit User Information")

        data = load_data(self.data_file_path)
        users = data.get("users", [])
       
        while True:
            username = input("Enter the username of the user to edit: ").strip()

            if not username:
                print("Username cannot be empty. Please enter a valid username.")
                continue
        
            user = next((u for u in users if u.get_username() == username), None)
            if user:
                print(f"Editing information for user: {user.get_username()}")
                print("\nEnter the new information or leave blank to keep the current value:")
            # get user input and update that user info
                updated_first_name = input("First name: ").strip()
                updated_last_name = input("Last name: ").strip()
                updated_email = input("email: ").strip()
                updated_emergency_contact_email = input("emergency contact email: ").strip()
            
            # TODO: validate the inputs
                if updated_first_name:
                    user.set_first_name(updated_first_name)
                if updated_last_name:
                    user.set_last_name(updated_last_name)
                if updated_email:
                    user.set_email(updated_email)
                if updated_emergency_contact_email:
                    user.set_emergency_contact(updated_emergency_contact_email)
            
                # set the update message based on whether the user update all the fields or not
                update_message = ""
                if not updated_first_name and not updated_last_name and not updated_email and not updated_emergency_contact_email:
                    update_message = "\nHere is your updated information (no changes made):"
                else:
                    update_message = '\nInfo updated successfully! Here is your updated information:'
                
                print(update_message)
                print_system_message(f"first name: {user.get_first_name()}\nlast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}")

                self.auth_service.users[username] = user
                self.auth_service.save_data_to_file()

                direct_to_dashboard()
                return
                
            else:
                print_system_message("User not found.")
                direct_to_dashboard()
                return
        
               


    def delete_user(self):
        pass

    def disable_user(self):
        pass

    def view_summary(self):
        pass

