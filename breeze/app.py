from breeze.services.auth_service import AuthService
from breeze.services.admin_service import AdminService
from breeze.services.patient_service.patient_service import PatientService
from breeze.services.mhwp_service import MHWPService

from breeze.utils.cli_utils import print_system_message, clear_screen
from breeze.utils.constants import BREEZE_BANNER_STRING, LOGIN_BANNER_STRING, REGISTER_BANNER_STRING

class BreezeApp:
    """BreezeApp: Manages the main user interface, including login, registration, and access 
                 to user-specific dashboards.
    """
    def __init__(self):
        self.auth_service = AuthService()
        self.admin_service = AdminService(self.auth_service)
        self.patient_service = PatientService(self.auth_service)
        self.mhwp_service = MHWPService(self.auth_service)
    
    def run(self):
        """Starts the application and displays the main menu.
        """
        self.show_main_menu()
        
    def show_main_menu(self):
        """Displays the main menu and processes user selection for login, registration, or exit.
           Clear out the user choice in each loop.
        """
        while True:
            print(BREEZE_BANNER_STRING)
            print("Welcome to Breeze - Mental Health Management System ! \n")
            print("[L]ogin")
            print("[R]egister")
            print("[E]xit")
            print()
            
            print("Please select an action from the options above (you can use any case):")
            user_choice = input("> ")
            
            match user_choice.lower():
                case "l":
                    clear_screen()
                    print(LOGIN_BANNER_STRING)
                    self.show_login()
                case "r":
                    clear_screen()
                    print(REGISTER_BANNER_STRING)
                    self.show_register()
                case "e":
                    clear_screen()
                    self.exit()
                case _:
                    clear_screen()
                    print_system_message("Invalid choice, try again!")   
                    self.show_main_menu()

    def show_login(self):
        """Prompts the user to log in, and redirects to the dashboard.
        """
        user = self.auth_service.login()
        if user:
            self.show_dashboard(user)
        else:
            print_system_message("Invalid credentials!\nType 'B' to go back to the main menu, or press any other key to try again.")
            user_input = input("> ")
            if user_input.strip().lower() == "b":
                clear_screen()
                self.show_main_menu()
            else:
                self.show_login()
    
    def show_register(self):
        """Prompts the user to register a new account and guides them to log in if successful.
        """
        new_user = self.auth_service.register()
        while new_user:
            user_input = input("> ")
            if user_input.strip().lower() == "b":
                clear_screen()
                self.show_main_menu()
                break
    
    def exit(self):
        """Displays a goodbye message and exits the application.
        """
        print_system_message("Bye!")
        exit()

    def show_dashboard(self, user):
        """Redirects the user to their respective dashboard based on role (Patient, Admin, or MHWP).

        Args:
            user (User): The user you going to redirect to their dashboard.
        """
        while True:
            clear_screen()
            if user.get_role() == 'Patient':
                logged_out = self.patient_service.show_patient_dashboard(user)
            elif user.get_role() == 'Admin':
                logged_out = self.admin_service.show_admin_dashboard(user)
            elif user.get_role() == "MHWP":
                logged_out = self.mhwp_service.show_mhwp_dashboard(user)
            else:
                print('Unknown user role')
            
            if logged_out:
                user = self.auth_service.logout()
                clear_screen()
                print_system_message("Logged out successully!")
                self.show_main_menu()
                break