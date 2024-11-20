import datetime
from breeze.utils.cli_utils import (
    clear_screen,
    print_system_message,
    direct_to_dashboard,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def record_mood(user, auth_service):
    """Records the patient's mood for the day."""
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print("Record Your Mood for the Day")
    print("Please choose a colour that best describes your mood:")
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
        colour_input = (
            input("Enter the colour code that represents your mood today: ")
            .strip()
            .lower()
        )
        if colour_input in colour_to_mood:
            mood_description = colour_to_mood[colour_input]
            comment = input(
                "Would you like to add any additional comments about your mood today? Type [R] to discard your entry: "
            ).strip()

            if comment.lower() == "r":
                print_system_message("Mood entry discarded. Returning to dashboard.")
                direct_to_dashboard()
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
