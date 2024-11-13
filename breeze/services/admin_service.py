from breeze.utils.cli_utils import print_system_message, clear_screen, direct_to_dashboard
from breeze.utils.constants import ADMIN_BANNER_STRING

class AdminService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
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
            case "d":
                self.delete_user()
            case "r":
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
        pass

    def delete_user(self):
        pass

    def disable_user(self):
        pass

    def view_summary(self):
        pass

