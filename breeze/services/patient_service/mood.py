from datetime import datetime
from breeze.models.mood_entry import MoodEntry
from breeze.utils.ansi_utils import colorise
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen,
    print_system_message,
    direct_to_dashboard,
)
from breeze.utils.constants import PATIENT_BANNER_STRING

mood_chart = {
    "G": {
        "name": "Green",
        "description": "Very Happy",
        "color_code": 40,
        "emoji": "\U0001F60A",
    },
    "L": {
        "name": "Light Green",
        "description": "Happy",
        "color_code": 120,
        "emoji": "\U0001F642",
    },
    "Y": {
        "name": "Yellow",
        "description": "Neutral",
        "color_code": 226,
        "emoji": "\U0001F610",
    },
    "O": {
        "name": "Orange",
        "description": "Sad",
        "color_code": 208,
        "emoji": "\U0001F641",
    },
    "R": {
        "name": "Red",
        "description": "Very Sad",
        "color_code": 160,
        "emoji": "\U0001F622",
    },
}


def record_mood(user, auth_service):
    """Records the patient's mood for the day."""
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(f"Hi, {user.get_username()}! Start record your mood for the day!")
    print("\nPlease choose a colour that best describes your mood:")
    for key, mood in mood_chart.items():
        mood_text = f"[{key}] {mood['name'].ljust(12)} - {mood['description']}"
        print(colorise(mood_text, color=mood["color_code"]) + f"  {mood['emoji']}")

    colour_to_mood = {
        "g": "Very Happy",
        "l": "Happy",
        "y": "Neutral",
        "o": "Sad",
        "r": "Very Sad",
    }

    while True:
        print(
            "\nEnter the colour code that represents your mood today (or enter [X] to exit without saving): "
        )
        colour_input = input("> ").strip().lower()
        if check_exit(colour_input):
            return

        if colour_input in colour_to_mood:
            mood_description = colour_to_mood[colour_input]
            print(
                "\nWould you like to add any additional comments about your mood today? (or enter [X] to exit without saving):"
            )
            comment = input("> ").strip()
            if check_exit(comment):
                return
            datetime_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            date_string = datetime.now().strftime("%d-%m-%Y")
            time_string = datetime.now().strftime("%H:%M:%S")
            new_mood = MoodEntry(mood_description, comment, date_string, time_string)
            if hasattr(user, "add_mood_entry"):
                user.add_mood_entry(
                    new_mood.get_mood_id(), mood_description, comment, datetime_str
                )
            auth_service.save_data_to_file()

            print_system_message("Mood recorded successfully!")
            direct_to_dashboard()
            return
        else:
            color_names = ", ".join(
                colorise(mood["name"], color=mood["color_code"])
                for mood in mood_chart.values()
            )
            print_system_message(
                f"Invalid color entered. Please choose from {color_names}."
            )
