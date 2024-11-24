import datetime
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen,
    direct_to_dashboard,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def enter_journal(user, auth_service):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(f"Hi {user.get_username()} !")
    print("Write your journal entry below, or enter [X] to exit without saving.")
    
    # title of the journal entry
    print("\nWhat is the title of your entry?")
    while True:
        journal_title = input("> ").strip()
        if check_exit(journal_title):
            return 
        if not journal_title:
            print_system_message("Your title is empty! Please try again!")
            continue
        else:
            break
        
    #  body of the journal entry
    print("\nWrite your journal entry below.")
    journal_body = input("> ").strip()
    if check_exit(journal_body):
        return
    
    # Allow the user to add more to their journal entry
    journal_additions = []
    while True:
        print("\nWould you like to add more? Type [S] to save if finished, or continue writing:")
        journal_addition = input("> ").strip()
        if check_exit(journal_addition):
            return
        if journal_addition.lower() == "s":
            break
        else:
            journal_additions.append(journal_addition)
            clear_screen()
            print(PATIENT_BANNER_STRING)
            print(journal_title)
            print(journal_body)
            print("\n".join(journal_additions))

    # Combine all parts of the journal entry
    journal_ent = journal_body + " " + " ".join(journal_additions)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save the journal entry
    if hasattr(user, "add_journal_entry"):
        user.add_journal_entry(journal_title, journal_ent, date_string)
        auth_service.save_data_to_file()
        direct_to_dashboard("Journal entry saved!")
    else:
        print_system_message(f"User {user.get_username()} not found in records!")
