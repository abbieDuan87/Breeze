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

        clear_screen()
        print(ADMIN_BANNER_STRING)
        print('Hi', user.get_username(), '!')
        print('What do you want to do today?')

        while True:
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

    def allocate_patient_to_mhwp(self):
        print_system_message('Feature to allocation to MHWP be implemented soon')

    def edit_user_information(self):
        print_system_message('Feature to edit user info coming soon')

    def delete_user(self):
        print_system_message('Feature to delete user coming soon')

    def disable_user(self):
        print_system_message('Feature to disable user coming soon')

    def view_summary(self):
        print_system_message('Feature view summary coming soon')

