from breeze.utils.cli_utils import (
    show_disabled_account_dashboard_menu,
    clear_screen
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def show_patient_dashboard(user, patient_service):
    """Displays the patient dashboard and processes user actions."""

    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)

        if user.get_is_disabled():
            return show_disabled_account_dashboard_menu(user.get_username())

        print(f"Hi {user.get_username()}!")
        print("What do you want to do today?")
        print("[E] Edit my personal information")
        print("[R] Record my mood for today")
        print("[J] Journal - enter new journaling text")
        print("[S] Search for meditation and relaxation exercises")
        print("[B] Book or cancel an appointment with my MHWP")
        print("[H] History - see my past journals, moods and appointments")
        print("[L] Learn more about mental health conditions and useful resources")
        print("[X] Log out")

        user_input = input("> ").strip().lower()

        if user_input in ["e", "r", "j", "s", "b", "h", "l", "x"]:
            if handle_user_choice(user_input, patient_service, user):
                return True


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
        case "h":
            patient_service.show_history(user)
        case "l":
            patient_service.learn_mental_health()     
        case "x":
            return True