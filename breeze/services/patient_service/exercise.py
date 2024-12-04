import time
from breeze.utils.ansi_utils import colorise
from breeze.utils.cli_utils import check_exit, clear_screen, print_system_message, direct_to_dashboard
from breeze.utils.constants import PATIENT_BANNER_STRING

def display_exercise_dashboard(valid_keywords):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print("Welcome to meditation and relaxation exercises!")

    print("\nChoose a sound you like from the following options:")
    for key, option in valid_keywords.items():
        print(f"- [{key.upper()}] {option['name']}")
    print("- [X] Exit")

def search_exercise():
    """Allows the patient to search for meditation and relaxation exercises with the ability to select multiple options."""
    valid_keywords = {
        "s": {"name": "Sleep", "path": "deep-sleep"},
        "p": {"name": "Piano", "path": "piano-meditation"},
        "r": {"name": "Rain", "path": "rain-and-thunder-sound-therapy"},
        "c": {"name": "Campfire", "path": "nature-sounds-campfire-and-stream"},
        "h": {"name": "Harp", "path": "i-see-you-harp"},
    }
    while True:
        display_exercise_dashboard(valid_keywords)
        choice = (
            input("\nSelect an option using the first letter or enter [X] to exit: ")
            .strip()
            .lower()
        )
        if check_exit(choice):
            return
        elif choice in valid_keywords:
            search_url = f"https://insighttimer.com/indiemusicbox/guided-meditations/{valid_keywords[choice]['path']}"
            print(
                f"Here is your selected meditation for '{valid_keywords[choice]['name']}':"
            )
            print_system_message(colorise(text=search_url, color=63, underline=True))
            time.sleep(3)
            direct_to_dashboard()
        else:
            print_system_message("Invalid choice. Please select a valid option.")
            time.sleep(1)
            
