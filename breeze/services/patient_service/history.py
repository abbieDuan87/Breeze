import json
import time
from math import ceil
from breeze.utils.data_utils import create_journal_entries_from_data, create_mood_entries_from_data, create_appointments_from_data, retrieve_variables_from_data, save_attr_data
from breeze.utils.cli_utils import clear_screen, print_system_message, print_journals, print_moods, check_exit
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

def delete_journal_entry(user, journal_id):
    journal_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'journals')
    try:
        journal_dicts = [journal for journal in journal_dicts if journal['id'] != journal_id]
        save_attr_data('data/users.json', user.get_username(), 'journals', journal_dicts)
        print('Entry deleted successfully.')
        data = create_journal_entries_from_data(journal_dicts)
        time.sleep(2)
    except IndexError:
        print_system_message('Invalid index. Please choose from available.')
        time.sleep(2)
        return
    return data

def delete_mood_entry(user, mood_id):
    mood_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'moods')
    try:
        mood_dicts = [mood for mood in mood_dicts if mood['id'] != mood_id]
        save_attr_data('data/users.json', user.get_username(), 'moods', mood_dicts)
        print('Entry deleted successfully.')
        data = create_mood_entries_from_data(mood_dicts)
        time.sleep(1)
    except IndexError:
        print_system_message('Invalid index. Please choose from available.')
        time.sleep(2)
        return
    return data


def filter_journal_results(data, search_term):
    filtered_list = []
    for journal in data:
        if search_term in journal.title.lower() or search_term in journal.entry.lower():
            filtered_list.append(journal)
    return filtered_list

def filter_mood_results(data, search_term):
    filtered_list = []
    for mood in data:
        if search_term in mood.mood.lower() or search_term in mood.comment.lower():
            filtered_list.append(mood)
    return filtered_list

def show_journal_history(user):
    # show the users journal entry in table format
    page_no = 1
    filtered = False
    while True: 
        clear_screen()
        print(PATIENT_BANNER_STRING)
        if filtered:
            journal_data = filter_journal_results(journal_data, search_filter)
            if not journal_data:
                print(f'There are no results with the search term {search_filter}. Returning...')
                time.sleep(3)
                filtered = False
                continue
        else:
            journal_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'journals')
        
        if not journal_dicts:
            print('\nYou currently have no journal entries!')
            print('Navigate to the Journaling tab on the dashboard to add your first!')
            print('Returning...')
            time.sleep(3)
            break
        else:
            if not filtered:
                journal_data = create_journal_entries_from_data(journal_dicts)
            if print_journals(journal_data, page_no):
                print(f'Page [{page_no}] of [{ceil(len(journal_data)/10)}]\n')
                print("[E] Edit a journal entry on this page")
                print("[D] Delete a journal entry on this page")
            
        valid_inputs = ["e", "d", "x"]
        
        if not filtered:
            print("[S] Search by title or text content")
            valid_inputs.append("s")  
        if len(journal_data) > page_no * 10:
            print("[N] See next page")
            valid_inputs.append("n")
        if page_no > 1:
            print("[P] See previous page")
            valid_inputs.append("p")
        if filtered:
            print("[R] Remove filter")
            valid_inputs.append("r")
        print("[X] Exit")
        user_input = input("> ").strip().lower()
        if check_exit(user_input):
            return
        if user_input not in valid_inputs:
            print_system_message("Invalid input. Please select from the options provided.")
            time.sleep(1)
            continue
        match user_input:
            case "s":
                print("Type a term to search by or quit using [X]:")
                while True:
                    search_filter = input("> ").strip().lower()
                    if search_filter == 'x':
                        break
                    else:
                        page_no = 1
                        filtered = True
                        break
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
                        print_system_message("An error occurred - invalid input.")
                        time.sleep(1)
                        break
            case "d":
                print("Enter the input of the entry you want to delete, or type X to exit")
                while True:
                    try:
                        journal_ind = input("> ").strip().lower()
                        index = int(journal_ind)
                        if not 0 < index <= 10:
                            print_system_message('Invalid index. Please choose from available.')
                            continue
                        entry = -(index + (page_no - 1) * 10)
                        try:
                            journal_to_delete = journal_data[entry].get_id()
                            journal_data = delete_journal_entry(user, journal_to_delete)
                        except IndexError:
                            print_system_message('Invalid index. Please choose from available.')
                            time.sleep(2)                        
                        break
                    except ValueError:
                        if journal_ind == "x":
                            break
                        print_system_message("An error occurred - invalid input.")
                        time.sleep(1)
                        break
            case "n":
                if "n" in valid_inputs:
                    page_no += 1
            case "p":
                if "p" in valid_inputs:
                    page_no -= 1
            case "r":
                filtered = False
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
    page_no = 1
    filtered = False
    while True: 
        clear_screen()
        print(PATIENT_BANNER_STRING)

        if filtered:
            mood_data = filter_mood_results(mood_data, search_filter)
            if not mood_data:
                print(f'There are no results with the search term {search_filter}. Returning...')
                time.sleep(3)
                filtered = False
                continue
        else:
            mood_dicts = retrieve_variables_from_data('data/users.json', user.get_username(), 'moods')
        
        if not mood_dicts:
            print('\nYou currently have no mood entries!')
            print('Navigate to the Mood tab on the dashboard to add your first!')
            print('Returning...')
            time.sleep(3)
            break
        else:
            if not filtered:
                mood_data = create_mood_entries_from_data(mood_dicts)
            if print_moods(mood_data, page_no):
                print(f'Page [{page_no}] of [{ceil(len(mood_data)/10)}]\n')
                print("[D] Delete a mood entry on this page")
        
        valid_inputs = ["d", "x"]

        if not filtered:
            print("[S] Search by title or text content")
            valid_inputs.append("s")  
        if len(mood_data) > page_no * 10:
            print("[N] See next page")
            valid_inputs.append("n")
        if page_no > 1:
            print("[P] See previous page")
            valid_inputs.append("p")
        if filtered:
            print("[R] Remove filter")
            valid_inputs.append("r")
        print("[X] Exit")
        user_input = input("> ").strip().lower()
        if check_exit(user_input):
            return
        if user_input not in valid_inputs:
            print_system_message("Invalid input. Please select from the options provided.")
            time.sleep(1)
            continue
        match user_input:
            case "s":
                print("Type a term to search by or quit using [X]:")
                while True:
                    search_filter = input("> ").strip().lower()
                    if search_filter == 'x':
                        break
                    else:
                        page_no = 1
                        filtered = True
                        break
            case "d":
                print("Enter the input of the entry you want to delete, or type X to exit")
                while True:
                    try:
                        mood_ind = input("> ").strip().lower()
                        index = int(mood_ind)
                        if not 0 < index <= 10:
                            print_system_message('Invalid index. Please choose from available.')
                            continue
                        entry = -(index + (page_no - 1) * 10)
                        try:
                            mood_to_delete = mood_data[entry].get_mood_id()
                            mood_data = delete_mood_entry(user, mood_to_delete)
                        except IndexError:
                            print_system_message('Invalid index. Please choose from available.')
                            time.sleep(2)                        
                        break
                    except ValueError:
                        if mood_ind == "x":
                            break
                        print_system_message("An error occurred - invalid input.")
                        time.sleep(1)
                        break
            case "n":
                if "n" in valid_inputs:
                    page_no += 1
            case "p":
                if "p" in valid_inputs:
                    page_no -= 1
            case "r":
                filtered = False
            case "x":
                return
            case _:
                print("An error occurred - invalid input.")
                time.sleep(1)
                continue

def show_history(user):
    
    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f"Hi {user.get_username()}!")
        print("What would you like to see?")
        print("[A] Appointments - see my appointment history")
        print("[M] Mood - view and delete my past mood entries")
        print("[J] Journal - view, edit and delete my past journal entries")
        print("[X] Exit\n")

        user_input = input("> ").strip().lower()
        if check_exit(user_input):
            return
        match user_input:
            case 'a':
                show_appointment_history(user)
            case 'm':
                show_mood_history(user)
            case 'j':
                show_journal_history(user)
            case '_':
                print_system_message('Invalid input. Please try again.')
                time.sleep(1)


