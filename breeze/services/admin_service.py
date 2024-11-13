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
        print('[D] Delete a user')
        print('[I] Disable a user')
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
            case "i":
                self.disable_user(user)
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

    def disable_user(self, user):
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print(f'Hi {user.get_username()} ! Here are all the users:')
        self._print_users_with_disabled_status()
        
        while True:
            print("Enter the username of the account that you want to disable (case insensitive), or press [R] to cancel:")        
            user_input = input("> ").strip().lower()
            if user_input == "r":
                break
            elif not user_input in self.auth_service.get_all_users(): # TODO: not allow user with username r.
                print_system_message(f"Username '{user_input}' not found! Please try again")
            else:
                user_to_disable = self.auth_service.get_all_users().get(user_input) # get the user by username
                if user_to_disable.get_is_disabled(): 
                    print_system_message(f"The account '{user_input}' is already disabled.")
                else:  
                    user_to_disable.set_is_disabled(True) # disable the user
                    self.auth_service.save_data_to_file() # save the change
                    print_system_message(f"The account '{user_input}' has been successfully disabled.")
                break
                
        direct_to_dashboard()
        
    def view_summary(self):
        pass

    def _print_users_with_disabled_status(self):
        """Private method that prints a list of all users and their account disabled status.
        
        This method is intended for AdminService class only and is responsible for displaying
        usernames, their roles, and whether their accounts are disabled. It excludes 
        users with the 'Admin' role from the list.

        Only the status of disabled accounts is shown for each user.

        Note:
            This is a private method and should not be accessed directly outside of 
            this class.
        """
        users = self.auth_service.get_all_users().values()
        
        print("-" * 65)  
        print(f"| {'Username':<20} | {'Role':<15} | {'Is Account Disabled':<20} |")
        print("-" * 65)  

        # Print each user's details with vertical lines
        for user in users:
            if not user.get_role() == 'Admin':
                username = user.get_username()
                role = user.get_role()
                is_account_disabled = "True" if user.get_is_disabled() else "False"
                print(f"| {username:<20} | {role:<15} | {is_account_disabled:<20} |")
        
        print("-" * 65)  