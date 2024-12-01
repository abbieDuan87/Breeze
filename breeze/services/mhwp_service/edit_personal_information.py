from breeze.utils.cli_utils import check_exit, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import MHWP_BANNER_STRING


def edit_personal_information(user, auth_service):
        """
        Allows the MHWP to edit their personal information.
        """
        clear_screen()
        print(MHWP_BANNER_STRING)
        print(f"Hi {user.get_username()}! Please update your personal information here.")
        print("\nHere is your current information:")
        print_system_message(
            f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nEmail: {user.get_email()}"
        )

        print("\nEnter the new information or leave blank to keep the current value (or enter [X] to exit without saving):\n")

        updated_first_name = input("First name: ").strip()
        if check_exit(updated_first_name):
            return

        updated_last_name = input("Last name: ").strip()
        if check_exit(updated_last_name):
            return

        updated_email = input("Email: ").strip()
        if check_exit(updated_email):
            return
        
        clear_screen()
        print(MHWP_BANNER_STRING)

        if updated_first_name:
            user.set_first_name(updated_first_name)
        if updated_last_name:
            user.set_last_name(updated_last_name)
        if updated_email:
            user.set_email(updated_email)

        if updated_first_name or updated_last_name or updated_email:
            update_message = "\nInfo updated successfully! Here is your updated information:"
        else:
            update_message = "\nHere is your updated information (no changes made):"

        print(update_message)
        print_system_message(f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}")

        auth_service.save_data_to_file()
        direct_to_dashboard()