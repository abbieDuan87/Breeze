from breeze.utils.data_utils import create_journal_entries_from_data, create_appointments_from_data
from breeze.utils.cli_utils import clear_screen, print_system_message
from breeze.utils.constants import PATIENT_BANNER_STRING

def show_journal_history(user):
    # show the users journal entry in table format
    pass

def show_appointment_history(user):
    # show users past appointments
    pass

def show_mood_history(user):
    # show users past mood entries in table format
    pass

def show_history(user):
    
    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f"Hi {user.get_username()}!")
        print("What would you like to see?")
        print("[A] Appointments - see my appointment history")
        print("[M] Mood - view, edit and delete my past mood entries")
        print("[J] Journal - view, edit and delete my past journal entries")
        print("[X] Return\n")

        user_input = input("> ").strip().lower()

        match user_input:
            case 'a':
                show_appointment_history(user)
            case 'm':
                show_mood_history(user)
            case 'j':
                show_journal_history(user)
            case 'x':
                return


