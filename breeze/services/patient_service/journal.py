from datetime import datetime, time, date
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen,
    direct_to_dashboard,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING
from breeze.models.journal_entry import JournalEntry

def display_journal_screen(user, title=None, body=None):
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(f"Hi {user.get_username()} !")
    print("Write your journal entry below, or enter [X] to exit without saving.")
    if title:
        print("\n" + title)
    if body:
        print("\n" + body)

def enter_journal(user, auth_service):
    display_journal_screen(user, title="What is the title of your entry?")
    # title of the journal entry
    while True:
        journal_title = input("> ").strip()
        if check_exit(journal_title):
            return 
        if not journal_title:
            print_system_message("Your title is empty! Please try again!")
            continue
        else:
            title = journal_title
            break
        
    #  body of the journal entry
    display_journal_screen(user, title=title)
    print("\nWrite your body below:")
    journal_body = input("> ").strip()
    if check_exit(journal_body):
        return
    
    # Allow the user to add more to their journal entry
    display_journal_screen(user, title=title, body=journal_body)
    while True:
        print("\nWould you like to add more? Type [S] to save your entry, or continue writing:")
        journal_addition = input("> ").strip()
        if check_exit(journal_addition):
            return
        if journal_addition.lower() == "s":
            break
        else:
            journal_body = journal_body + "\n" + journal_addition
            display_journal_screen(user,title=title,body=journal_body)

    # Combine all parts of the journal entry
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_string = datetime.now().strftime("%Y-%m-%d")
    time_string = datetime.now().strftime("%H:%M:%S")
    new_entry = JournalEntry(journal_title, journal_body, date_string, time_string)
    # Save the journal entry
    if hasattr(user, "add_journal_entry"):
        user.add_journal_entry(new_entry.get_id(), journal_title, journal_body, datetime_str)
        auth_service.save_data_to_file()
        display_journal_screen(user, title=title, body=journal_body)
        direct_to_dashboard("Journal entry saved! You may view and add to your entry via [H] History")
    else:
        print_system_message(f"User {user.get_username()} not found in records!")
