from breeze.utils.cli_utils import check_exit, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import PATIENT_BANNER_STRING


def edit_personal_information(user, auth_service):
    """
    Allows the user to edit their personal information.
    The user can press [X] at any time to exit without saving changes.
    """
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(
        f"Hi {user.get_username()}! Please update your personal information or press [X] to exit without saving."
    )
    print("\nHere is your current information:")
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}"
    )

    print("\nEnter the new information or leave blank to keep the current value:")

    updated_first_name = input("First name: ").strip()
    if check_exit(updated_first_name):
        return

    updated_last_name = input("Last name: ").strip()
    if check_exit(updated_last_name):
        return

    updated_email = input("Email: ").strip()
    if check_exit(updated_email):
        return

    updated_emergency_contact_email = input("Emergency contact email: ").strip()
    if check_exit(updated_emergency_contact_email):
        return

    # Update the user's information if valid inputs were provided
    if updated_first_name:
        user.set_first_name(updated_first_name)
    if updated_last_name:
        user.set_last_name(updated_last_name)
    if updated_email:
        user.set_email(updated_email)
    if updated_emergency_contact_email:
        user.set_emergency_contact(updated_emergency_contact_email)

    # Set the update message based on whether the user updated any fields
    update_message = (
        "\nInfo updated successfully! Here is your updated information:"
        if any([updated_first_name, updated_last_name, updated_email, updated_emergency_contact_email])
        else "\nHere is your updated information (no changes made):"
    )

    print(update_message)
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}"
    )

    auth_service.save_data_to_file()
    direct_to_dashboard()
