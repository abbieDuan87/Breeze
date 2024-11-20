from breeze.utils.cli_utils import clear_screen, print_system_message
from breeze.utils.constants import PATIENT_BANNER_STRING


def search_exercise():
    """Allows the patient to search for meditation and relaxation exercises with the ability to select multiple options."""
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print_system_message("Search for Meditation and Relaxation Exercises")

    valid_keywords = {
        "s": {"name": "Sleep", "path": "deep-sleep"},
        "p": {"name": "Piano", "path": "piano-meditation"},
        "r": {"name": "Rain", "path": "rain-and-thunder-sound-therapy"},
        "c": {"name": "Campfire", "path": "nature-sounds-campfire-and-stream"},
        "h": {"name": "Harp", "path": "i-see-you-harp"},
    }

    print_system_message("Choose a sound you like from the following options:")
    for key, option in valid_keywords.items():
        print(f"- [{key.upper()}] {option['name']}")
    print("- [X] Exit")

    while True:
        print()
        choice = (
            input("Select an option using the first letter or [X] to exit: ")
            .strip()
            .lower()
        )
        if choice == "x":
            print_system_message("Exiting to the dashboard...")
            clear_screen()
            break
        elif choice in valid_keywords:
            search_url = f"https://insighttimer.com/indiemusicbox/guided-meditations/{valid_keywords[choice]['path']}"
            print_system_message(
                f"Here is your selected meditation for '{valid_keywords[choice]['name']}':"
            )
            print(search_url)
        else:
            print_system_message("Invalid choice. Please select a valid option.")