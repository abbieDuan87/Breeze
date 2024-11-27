from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.utils.cli_utils import check_exit, check_previous, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import ADMIN_BANNER_STRING
from breeze.utils.print_patinet_utils import _print_users, _print_users_with_disabled_status


def edit_user_information(auth_service):
    """
    Allows admin to edit information for a patient or an MHWP.
    
    Args:
        auth_service (AuthService): The authentication service managing users.
    """
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("Edit User Information")

    while True:
        print("\nDo you want to edit information for a Patient or an MHWP?\nEnter [P] for Patient or [M] for MHWP (or [X] to exit):")
        user_input = input("> ").strip().lower()

        if check_exit(user_input):
            return
        if user_input in ["p", "m"]:
            break
        print_system_message("Invalid choice. Please select a valid option.")

    # Filter and display users of the chosen type
    users_to_edit = [
        user for user in auth_service.users.values() if (isinstance(user, Patient) if user_input == "p"
        else isinstance(user, MHWP))
    ]
    title = "Patients" if user_input == "p" else "MHWPs"

    clear_screen()
    print(ADMIN_BANNER_STRING)
    _print_users(users_to_edit, title)

    while True:
        print("\nEnter the username of the user to edit (or enter [R] to return to previous menu):")
        username = input("> ").strip().lower()
        
        if check_previous(username):
            break

        user = auth_service.users.get(username)
        if not user:
            print_system_message("Invalid username. Please try again.")
            continue

        # Display and edit user information
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print(f"Editing information for user: {user.get_username()}")
        current_info = (
            f"First name: {user.get_first_name()}\n"
            f"Last name: {user.get_last_name()}\n"
            f"Email: {user.get_email()}\n"
        )
        if isinstance(user, Patient):
            current_info += f"Emergency contact email: {user.get_emergency_contact()}\n"
        print_system_message(current_info)

        print("\nEnter new information or leave blank to keep current values:")
        updated_first_name = input("First name: ").strip()
        updated_last_name = input("Last name: ").strip()
        updated_email = input("Email: ").strip()
        updated_emergency_contact_email = (
            input("Emergency contact email: ").strip() if isinstance(user, Patient) else None
        )

        # Update user information
        if updated_first_name:
            user.set_first_name(updated_first_name)
        if updated_last_name:
            user.set_last_name(updated_last_name)
        if updated_email:
            user.set_email(updated_email)
        if updated_emergency_contact_email:
            user.set_emergency_contact(updated_emergency_contact_email)

        auth_service.save_data_to_file()
        print_system_message("User information updated successfully.")
        direct_to_dashboard()
        return


def delete_user(auth_service):
    """
    Deletes a user from the system.
    
    Args:
        auth_service (AuthService): The authentication service managing users.
    """
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("Delete a User")

    _print_users(auth_service.users.values(), "All Users")

    while True:
        print("\nEnter the username of the user to delete (or press [X] to exit):")
        username = input("> ").strip().lower()

        if check_exit(username):
            break

        user_to_delete = auth_service.users.get(username)
        if not user_to_delete:
            print_system_message("Invalid username. Please try again.")
            continue

        if user_to_delete.get_role() == "Admin":
            print_system_message("Admin accounts cannot be deleted.")
            continue

        print_system_message(f"Are you sure you want to delete the user '{username}'? Type [Y] to confirm or [N] to cancel:")
        confirmation = input("> ").strip().lower()
        if confirmation == "y":
            del auth_service.users[username]
            auth_service.save_data_to_file()
            print_system_message(f"User '{username}' has been successfully deleted.")
            direct_to_dashboard()
            return
        elif confirmation == "n":
            print_system_message("Deletion canceled. You can try another username or exit.")
        else:
            print_system_message("Invalid input. Please type [Y] to confirm or [N] to cancel.")


def disable_user(auth_service):
    """
    Toggles a user's account status (enable/disable).
    
    Args:
        auth_service (AuthService): The authentication service managing users.
    """
    
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("Toggle User Status (Enable/Disable)")

    while True:
        _print_users_with_disabled_status(auth_service)
        
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
        print_system_message(f"Account '{username}' has been successfully {action}.")
        continue