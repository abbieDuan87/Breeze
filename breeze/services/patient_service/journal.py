from datetime import datetime, time, date
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen,
    direct_to_dashboard,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING
from breeze.models.journal_entry import JournalEntry

def print_journal_dashboard(user, title=None, body=None):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(f"Hi {user.get_username()} !")
    print("Write your journal entry below, or enter [X] to exit without saving.\n")
    if title: 
        print(title)
    if body:
        print("\n" + body)

def enter_journal(user, auth_service):
    error = False
    while True:
        print_journal_dashboard(user)
        # title of the journal entry
        print("What is the title of your entry?")
        if error:
            print_system_message("Your title is empty! Please try again!")
        journal_title = input("> ").strip()
        if check_exit(journal_title):
            return 
        if not journal_title:
            error = True
            continue
        else:
            break
        
    #  body of the journal entry
    print_journal_dashboard(user, title=journal_title)
    print("\nWrite your journal entry below.")
    journal_body = input("> ").strip()
    if check_exit(journal_body):
        return
   
    while True:
        print_journal_dashboard(user, title=journal_title, body=journal_body)
        print("\nWould you like to add more? Type [S] to save if finished, or continue writing:")
        journal_addition = input("> ").strip()
        if check_exit(journal_addition):
            return
        if journal_addition.lower() == "s":
            break
        else:
            journal_body = journal_body + "\n" + journal_addition

    # Combine all parts of the journal entry
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_string = datetime.now().strftime("%Y-%m-%d")
    time_string = datetime.now().strftime("%H:%M:%S")
    new_entry = JournalEntry(journal_title, journal_body, date_string, time_string)
    # Save the journal entry
    if hasattr(user, "add_journal_entry"):
        user.add_journal_entry(new_entry.get_id(), journal_title, journal_body, datetime_str)
        auth_service.save_data_to_file()
        direct_to_dashboard("Journal entry saved!")
    else:
        print_system_message(f"User {user.get_username()} not found in records!")
