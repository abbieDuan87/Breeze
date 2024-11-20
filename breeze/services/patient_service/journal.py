import datetime
from breeze.utils.cli_utils import (
    clear_screen,
    direct_to_dashboard,
    print_system_message,
    return_to_previous,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def enter_journal(user, auth_service):
    # Include util 'print system message'
    # Include all funcs from data utils to load/save entry to json file
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print(f"Hi {user.get_username()} !")
    print_system_message(
        "Write your journal entry below, or enter [R] at any time to return to the previous page without saving"
    )
    print_system_message("What is the title of your entry?")
    invalid_title = True
    while invalid_title:
        journal_title = input().strip()
        if return_to_previous(journal_title, "r"):
            return
        if not journal_title:
            print_system_message("Your title is empty! Please try again!")
            continue
        else:
            break
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print_system_message(
        "Write your journal entry below, or enter [R] at any time to return to the previous page without saving: \n"
    )
    print(journal_title)
    print_system_message("Write your journal entry here:")
    journal_body = input("").strip()
    clear_screen()
    print(PATIENT_BANNER_STRING)
    print_system_message(
        "Write your journal entry below, or enter [R] at any time to return to the previous page without saving: \n"
    )
    print(journal_title)
    print(journal_body)
    if journal_body.strip() == "":
        direct_to_dashboard("Entry is empty!")
        return
    if return_to_previous(journal_body, "r"):
        return
    journal_additions = []
    in_progress = True
    while in_progress:
        print_system_message(
            "Would you like to write more? Type [N] if finished, or continue writing:"
        )
        journal_addition = input("").strip()
        if return_to_previous(journal_addition, "r"):
            return
        if journal_addition.lower() == "n":
            in_progress = False
        else:
            journal_additions.append(journal_addition)
            clear_screen()
            print(PATIENT_BANNER_STRING)
            print_system_message(
                "Write your journal entry below, or enter [R] at any time to return to the previous page without saving: \n"
            )
            print(journal_title)
            print(journal_body)
            print("\n".join(journal_additions))

    journal_ent = journal_body + " " + " ".join(journal_additions)
    date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"title": journal_title, "text": journal_ent, "date": date_string}
    if hasattr(user, "add_journal_entry"):
        # save file to users.json
        user.add_journal_entry(journal_title, journal_ent, date_string)
        auth_service.save_data_to_file()
        clear_screen()
        print(PATIENT_BANNER_STRING)
        direct_to_dashboard("Journal entry saved!")
        return
    print_system_message(f"User {user} not in records!")
    datetime.time.sleep(2)
    return
