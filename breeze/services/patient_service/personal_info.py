<<<<<<< HEAD
from breeze.utils.cli_utils import check_exit, clear_screen, direct_to_dashboard, print_system_message, is_valid_name, is_invalid_email, is_empty
=======
import time

from breeze.utils.cli_utils import check_exit, clear_screen, direct_to_dashboard, print_system_message, is_invalid_email
>>>>>>> main
from breeze.utils.constants import PATIENT_BANNER_STRING


def show_default_layout(user, addon=0):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(
        f"Hi {user.get_username()}! Please update your personal information here."
    )
    print("\nHere is your current information:")
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nEmail: {user.get_email()}\nGender: {user.get_gender()}\nEmergency contact email: {user.get_emergency_contact()}"
    )
    print("\nEnter the new information or leave blank to keep the current value (or enter [X] to exit without saving):\n")
    if addon:
        print(addon)

<<<<<<< HEAD
    while True:
        updated_first_name = input("First name: ").strip()
        if is_valid_name(updated_first_name):
            break
        elif check_exit(updated_first_name):
            return

    while True:
        updated_last_name = input("Last name: ").strip()
        if is_valid_name(updated_last_name):
            break
        elif check_exit(updated_last_name):
            return
        
    while True:
        updated_email = input("Email: ").strip()
        if is_invalid_email(updated_email):
            continue
        elif check_exit(updated_email):
            return
        else:
            break

    while True:
        updated_emergency_contact_email = input("Emergency contact email: ").strip()
        if is_invalid_email(updated_emergency_contact_email):
            continue
        elif check_exit(updated_emergency_contact_email):
            return
        else:
            break
=======
def edit_personal_information(user, auth_service):
    """
    Allows the user to edit their personal information.
    The user can press [X] at any time to exit without saving changes.
    """
    show_default_layout(user)
    updated_first_name = input("First name: ").strip()
    if check_exit(updated_first_name):
        return

    updated_last_name = input("Last name: ").strip()
    if check_exit(updated_last_name):
        return
>>>>>>> main
    
    addon = f"First name: {updated_first_name}\nLast name: {updated_last_name}"  

    while True:
        show_default_layout(user, addon=addon)
        updated_email = input("Email: ").strip()
        if check_exit(updated_email):
            return
        if updated_email and is_invalid_email(updated_email):
            time.sleep(1)
            continue
        else:
            addon = addon + f'\nEmail: {updated_email}'
            break
    
    gender_dict = {
        'm' : 'Male',
        'f' : 'Female',
        'n' : 'Non-binary',
        't' : 'Transgender',
        'o' : 'Other'
    }
    while True:
        show_default_layout(user, addon=addon)
        print("Gender Options:\n[M] Male\n[F] Female\n[N] Non-binary\n[T] Transgender\n[O] Other")
        updated_gender = input("Gender: ").strip().lower()
        if updated_gender and updated_gender not in gender_dict.keys():
            print_system_message("Please select a valid option.")
            time.sleep(1)
            continue
        elif updated_gender:
            updated_gender = gender_dict[updated_gender]
            addon = addon + f'\nGender: {updated_gender}'
            break
        else:
            addon = addon + f'\nGender: {updated_gender}'
            break
    
    while True:
        show_default_layout(user, addon=addon)
        updated_emergency_contact_email = input("Emergency contact email: ").strip()
        if check_exit(updated_emergency_contact_email):
            return
        if updated_emergency_contact_email and is_invalid_email(updated_emergency_contact_email):
            time.sleep(1)
            continue
        else:
            break

    clear_screen()
    print(PATIENT_BANNER_STRING)

    if updated_first_name:
        user.set_first_name(updated_first_name)
    if updated_last_name:
        user.set_last_name(updated_last_name)
    if updated_email:
        user.set_email(updated_email)
    if updated_gender:
        user.set_gender(updated_gender)
    if updated_emergency_contact_email:
        user.set_emergency_contact(updated_emergency_contact_email)

    update_message = (
        "\nInfo updated successfully! Here is your updated information:"
        if any([updated_first_name, updated_last_name, updated_email, updated_emergency_contact_email])
        else "\nHere is your updated information (no changes made):"
    )

    print(update_message)
    print_system_message(
        f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nEmail: {user.get_email()}\nGender: {user.get_gender()}\nEmergency contact email: {user.get_emergency_contact()}"
    )

    auth_service.save_data_to_file()
    direct_to_dashboard()
