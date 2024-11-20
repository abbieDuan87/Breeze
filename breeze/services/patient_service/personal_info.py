from breeze.utils.cli_utils import clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import PATIENT_BANNER_STRING


def edit_personal_information(user, auth_service):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(
        f"Hi {user.get_first_name()} (username: {user.get_username()}) ! Please update your personal information"
    )
    print("Here is your current information:")
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}"
    )

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
    if (
        not updated_first_name
        and not updated_last_name
        and not updated_email
        and not updated_emergency_contact_email
    ):
        update_message = "\nHere is your updated information (no changes made):"
    else:
        update_message = (
            "\nInfo updated successfully! Here is your updated information:"
        )

    print(update_message)
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}"
    )

    # Save the changes to the file via AuthService
    auth_service.save_data_to_file()

    direct_to_dashboard()
