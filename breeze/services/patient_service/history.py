import json
import time
from breeze.utils.data_utils import create_journal_entries_from_data, create_appointments_from_data, retrieve_variables_from_data, save_attr_data
from breeze.utils.cli_utils import clear_screen, print_system_message, print_journals
from breeze.utils.constants import PATIENT_BANNER_STRING

def edit_journal_data(user, entry, page):
    pass
    # if not 0 < entry <= 10:
    #     print('Invalid index. Please choose from available.')
    #     return
    # entry = -(entry + (page - 1) * 10)
    # print(entry)
    # journal_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'journals')
    # journal_data = create_journal_entries_from_data(journal_dicts)
    # try:
    #     journal = journal_data[::-1][entry]
    # except IndexError:
    #     print('Invalid index. Please choose from available.')
    #     return
    # print(journal)
    # time.sleep(5)

def delete_journal_entry(user, entry, page):
    if not 0 < entry <= 10:
        print('Invalid index. Please choose from available.')
        return
    entry = -(entry + (page - 1) * 10)
    journal_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'journals')
    try:
        journal_dicts.pop(entry)
        save_attr_data('data/users.json', user.get_username(), 'journals', journal_dicts)
        print('Entry deleted successfully.')
        time.sleep(2)
    except IndexError:
        print('Invalid index. Please choose from available.')
        time.sleep(2)
        return

def show_journal_history(user):
    # show the users journal entry in table format
    page_no = 1
    while True: 
        clear_screen()
        print(PATIENT_BANNER_STRING)
        journal_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'journals')
        if not journal_dicts:
            print('\nYou currently have no journal entries!')
            print('Navigate to the Journaling tab on the dashboard to add your first!')
            time.sleep(3)
            break
        else:
            journal_data = create_journal_entries_from_data(journal_dicts)
            if print_journals(journal_data, page_no):
                print("\n[E] Edit a journal entry on this page")
                print("[D] Delete a journal entry on this page")

        valid_inputs = ["x"]
        if len(journal_data) > page_no * 10:
            print("[N] See next page")
            valid_inputs.append("n")
        if page_no > 1:
            print("[P] See previous page")
            valid_inputs.append("p")
        print("[X] Exit")
        user_input = input("> ").strip().lower()

        match user_input:
            case "e":
                print("Enter the input of the entry you want to edit, or type X to exit")
                while True:
                    journal_ind = input("> ").strip().lower()
                    try:
                        index = int(journal_ind)
                        edit_journal_data(user, index, page_no)
                    except ValueError:
                        if journal_ind == "x":
                            break
                        print("An error occurred - invalid input.")
            case "d":
                print("Enter the input of the entry you want to delete, or type X to exit")
                while True:
                    try:
                        journal_ind = input("> ").strip().lower()
                        index = int(journal_ind)
                        delete_journal_entry(user, index, page_no)
                        break
                    except ValueError:
                        if journal_ind == "x":
                            break
                        print("An error occurred - invalid input.")
            case "n":
                if "n" in valid_inputs:
                    page_no += 1
            case "p":
                if "p" in valid_inputs:
                    page_no -= 1
            case "x":
                return
            case _:
                print("An error occurred - invalid input.")
                time.sleep(1)
                continue

    
        

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
        print("[X] Exit\n")

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


