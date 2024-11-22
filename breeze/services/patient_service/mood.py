import datetime
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen,
    print_system_message,
    direct_to_dashboard,
)
from breeze.utils.constants import PATIENT_BANNER_STRING

def record_mood(user, auth_service):
    """Records the patient's mood for the day."""
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print("Record your mood for the day. Press [X] to exit without saving.")
    print("\nPlease choose a colour that best describes your mood:")
    print("[G]reen - Very Happy")
    print("[L]ight Green - Happy")
    print("[Y]ellow - Neutral")
    print("[O]range - Sad")
    print("[R]ed - Very Sad")

    colour_to_mood = {
        "g": "Very Happy",
        "l": "Happy",
        "y": "Neutral",
        "o": "Sad",
        "r": "Very Sad",
    }

    while True:
        print("\nEnter the colour code that represents your mood today: ")
        colour_input = (input("> ").strip().lower())
        if check_exit(colour_input, "Exiting mood recording without saving..."):
            return

        if colour_input in colour_to_mood:
            mood_description = colour_to_mood[colour_input]
            print("\nWould you like to add any additional comments about your mood today?")
            comment = input("> ").strip()
            if check_exit(comment, "Exiting mood recording without saving..."):
                return 

            date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if hasattr(user, "add_mood_entry"):
                user.add_mood_entry(mood_description, comment, date_string)
            auth_service.save_data_to_file()

            print_system_message("Mood recorded successfully!")
            direct_to_dashboard()
            return
        else:
            print_system_message(
                "Invalid colour entered. Please choose from Green, Light Green, Yellow, Orange, or Red."
            )