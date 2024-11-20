from breeze.utils.cli_utils import (
    print_system_message,
    show_disabled_account_dashboard_menu,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def show_patient_dashboard(user, patient_service):
    """Displays the patient dashboard and processes user actions."""
    print(PATIENT_BANNER_STRING)

    if user.get_is_disabled():
        return show_disabled_account_dashboard_menu(user.get_username())

    print(f"Hi {user.get_username()}!")
    print("What do you want to do today?")
    print("[E] Edit my personal information")
    print("[R] Record my mood for today")
    print("[J] Journal - enter your journaling text")
    print("[S] Search for meditation and relaxation exercises")
    print("[B] Book or cancel an appointment with my MHWP")
    print("[X] Log out")

    user_input = input("> ").strip().lower()
    return handle_user_choice(user_input, patient_service, user)


def handle_user_choice(user_input, patient_service, user):
    """Handles user input and calls the appropriate functions."""
    match user_input:
        case "e":
            patient_service.edit_personal_information(user)
        case "r":
            patient_service.record_mood(user)
        case "j":
            patient_service.enter_journaling(user)
        case "s":
            patient_service.search_exercise(user)
        case "b":
            patient_service.manage_appointment(user)
        case "x":
            return True  # Log out
        case _:
            print_system_message("Invalid choice. Please try again.")
    return False
