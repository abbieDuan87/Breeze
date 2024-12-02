from breeze.services.admin_service.admin_user_printer import print_users_with_disabled_status
from breeze.utils.cli_utils import check_exit, clear_screen, print_system_message, direct_to_dashboard
from breeze.utils.constants import ADMIN_BANNER_STRING


def disable_user(auth_service):
    """
    Toggles a user's account status (enable/disable).
    
    Args:
        auth_service (AuthService): The authentication service managing users.
    """
    
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("Toggle User Status (Enable/Disable)")

    print_users_with_disabled_status(auth_service)

    while True:
        print("\nEnter the username of the account to toggle status (or press [X] to exit):")
        username = input("> ").strip().lower()

        if check_exit(username):
            return

        user_to_toggle = auth_service.users.get(username)
        if not user_to_toggle:
            print_system_message("Invalid username. Please try again.")
            continue

        if user_to_toggle.get_role() == "Admin":
            print_system_message("Admin accounts cannot be enabled or disabled.")
            continue

        if user_to_toggle.get_is_disabled():
            user_to_toggle.set_is_disabled(False)
            action = "enabled"
        else:
            user_to_toggle.set_is_disabled(True)
            action = "disabled"

        auth_service.save_data_to_file()
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print_system_message("Toggle User Status (Enable/Disable)")
        print_users_with_disabled_status(auth_service)
        print_system_message(f"Account '{username}' has been successfully {action}.")
        direct_to_dashboard()
        return