from breeze.utils.cli_utils import clear_screen
from breeze.utils.constants import ADMIN_BANNER_STRING

    
def show_admin_dashboard(user, admin_service):
    """
    Displays the admin dashboard and processes user actions.

    Args:
        user (User): _The logged-in user
        
    Returns:
        bool: True if the user chose to log out, otherwise False
    """
    while True:
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print('Hi', user.get_username(), '!')
        print('What do you want to do today?')
        print('[R] Reallocate patient to MHWP')
        print('[E] Edit user information')
        print('[D] Delete a user')
        print('[I] Disable a user')
        print('[V] View summary')
        print('[X] Log out')

        user_input = input("> ").strip().lower()

        if user_input in ["r", "e", "d", "i", "v", "x"]: 
            match user_input:
                case "r":
                    admin_service.reallocate_patient_to_mhwp()
                case "e":
                    admin_service.edit_user_information()
                case "d":
                    admin_service.delete_user()
                case "i":
                    admin_service.disable_user()
                case "v":
                    admin_service.view_summary()
                case "x":
                    return True
                case _:
                    print("Invalid input. Please try again.")
