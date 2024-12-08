import json
import time
import datetime as dt
from math import ceil

from breeze.utils.data_utils import create_journal_entries_from_data, create_mood_entries_from_data
from breeze.utils.cli_utils import clear_screen, print_system_message, print_user_appointments, print_journals, print_moods, check_exit
from breeze.utils.constants import PATIENT_BANNER_STRING

def edit_journal_database(user, journal_data, edit_delete, page_no, auth_service):
    try:                      
        journal_ind = input("> ").strip().lower()
        index = int(journal_ind)
        if not 0 < index <= 10:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
            return journal_data
        entry = -(index + (page_no - 1) * 10)
        try:
            journal_id = journal_data[entry].get_id()
            if edit_delete == 'a':
                journal_data = edit_journal_data(user, journal_data, journal_id, entry, auth_service)
            else:
                journal_data = delete_journal_entry(user, journal_id, auth_service)
        except IndexError:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
            return journal_data
        return journal_data
    except ValueError:
        if journal_ind == "x":
            return journal_data
        print_system_message("An error occurred - invalid input.")
        time.sleep(1)
        return journal_data

def edit_journal_data(user, journal_data, journal_id, entry, auth_service):
    journal = journal_data[entry]
    entry = journal.entry
    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print_system_message(journal.title)
        print_system_message(entry) 
        print('Continue writing to append to your journal entry, enter [S] to save, or [X] to leave without saving:')
        addition = input("> ")
        if check_exit(addition):
            return journal_data
        if addition.lower() == "s":
            journal.set_entry(entry)    
            for journal_ent in user.get_journal_entries():
                if journal_ent['id'] == journal_id:
                    journal_ent['text'] = entry
                    journal_ent['last_update'] = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            auth_service.save_data_to_file()
            print('Entry edited successfully.')
            data = create_journal_entries_from_data(user.get_journal_entries())
            time.sleep(2)
            return data
        else:
            entry = entry + "\n" + addition

def view_entry(data, page_no):
    try:
        journal_ind = input("> ").strip().lower()
        index = int(journal_ind)
        if not 0 < index <= 10:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
        entry = -(index + (page_no - 1) * 10)
        try:
            viewed = data[entry]        
            while True:
                clear_screen()
                print(PATIENT_BANNER_STRING)
                print_system_message(viewed.title)
                print_system_message(viewed.entry)      
                print("Enter [X] to return to the previous page.")
                return_val= input("> ").strip().lower()
                if return_val == 'x': 
                    break
        except IndexError:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
    except ValueError:
        if journal_ind == "x":
            return
        print_system_message("An error occurred - invalid input.")
        time.sleep(1)
        return

def delete_journal_entry(user, journal_id, auth_service):
    user.delete_journal_entry(journal_id)
    auth_service.save_data_to_file()
    print('Entry deleted successfully.')
    data = create_journal_entries_from_data(user.get_journal_entries())
    time.sleep(2)
    return data

def delete_mood_entry(user, mood_id, auth_service):
    user.delete_mood_entry(mood_id)
    auth_service.save_data_to_file()
    print('Entry deleted successfully.')
    data = create_mood_entries_from_data(user.get_mood_entries())
    time.sleep(1)
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

def view_appt_summary(data, page_no):
    try:
        ind = input("> ").strip().lower()
        index = int(ind)
        if not 0 < index <= 10:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
        entry = -(index + (page_no - 1) * 10)
        try:
            viewed = data[entry]        
            while True:
                clear_screen()
                print(PATIENT_BANNER_STRING)
                print_system_message(viewed.mhwp_username)
                print_system_message(viewed.summary)      
                print("Enter [X] to return to the previous page.")
                return_val= input("> ").strip().lower()
                if return_val == 'x': 
                    break
        except IndexError:
            print_system_message('Invalid index. Please choose from available.')
            time.sleep(2)
    except ValueError:
        if ind == "x":
            return
        print_system_message("An error occurred - invalid input.")

def show_journal_history(user, auth_service):
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
            journal_dicts = user.get_journal_entries()
        
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
                print(f"Filtering by result: '{search_filter}'\n") if filtered else None
                print("[V] View a journal entry on this page")
                print("[A] Add to a journal entry on this page")
                print("[D] Delete a journal entry on this page")
            
        valid_inputs = ["v", "a", "d", "x"]
        
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
                print("Type a term to search by or quit using [X] (type 'X/' to filter by string 'X'):")
                while True:
                    search_filter = input("> ").strip().lower()
                    if search_filter == 'x':
                        break
                    else:
                        if search_filter == 'x/':
                            search_filter = 'x'
                        page_no = 1
                        filtered = True
                        break
            case "v":
                print("Enter the input of the entry you want to view, or type [X] to exit")
                view_entry(journal_data, page_no)
            case "a":
                print("Enter the input of the entry you want to edit, or type [X] to exit")    
                journal_data = edit_journal_database(user, journal_data, 'a', page_no, auth_service)
            case "d":
                print("Enter the input of the entry you want to delete, or type [X] to exit")
                journal_data = edit_journal_database(user, journal_data, 'd', page_no, auth_service)
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

def filter_appt_results(data, search_term):
    filtered_list = []
    for appt in data:
        if search_term in appt.summary.lower() or search_term in appt.mhwp_username.lower():
            filtered_list.append(appt)
    return filtered_list
    
def show_appointment_history(user):
    page_no = 1
    filtered = False
    while True: 
        clear_screen()
        print(PATIENT_BANNER_STRING)

        if filtered:
            appt_data = filter_appt_results(appt_data, search_filter)
            if not appt_data:
                print(f'There are no results with the search term {search_filter}. Returning...')
                time.sleep(3)
                filtered = False
                continue
        else:
            appt_data = []
            appts = user.get_appointments()
            for appt in appts:
                if appt.summary != None:
                    appt_data.append(appt)
        if not appt_data:
            print('\nYou currently have no appointments!')
            print('Navigate to the Appointment tab on the dashboard to schedule an appointment with your MHWP.')
            print('Returning...')
            time.sleep(3)
            break
        else:
            if print_user_appointments(appt_data):
                print(f'Page [{page_no}] of [{ceil(len(appt_data)/10)}]\n')
                print(f"Filtering by result: '{search_filter}'\n") if filtered else None
                print("[V] View an appointment on this page")
        
        valid_inputs = ["v", "x"]

        if not filtered:
            print("[S] Search by MHWP or summary content")
            valid_inputs.append("s")  
        if len(appt_data) > page_no * 10:
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
            case "v":
                print("Enter the input of the entry you want to view, or type [X] to exit")
                view_appt_summary(appt_data, page_no)
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

def show_mood_history(user, auth_service):
    page_no = 1
    filtered = False
    while True: 
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(user.get_mood_entries())

        if filtered:
            mood_data = filter_mood_results(mood_data, search_filter)
            if not mood_data:
                print(f'There are no results with the search term {search_filter}. Returning...')
                time.sleep(3)
                filtered = False
                continue
        else:
            mood_dicts = user.get_mood_entries()
        
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
                print(f"Filtering by result: '{search_filter}'\n") if filtered else None
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
                print("Enter the input of the entry you want to delete, or type [X] to exit")
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
                            mood_data = delete_mood_entry(user, mood_to_delete, auth_service)
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

def show_history(user, auth_service):
    
    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f"Hi {user.get_username()}!")
        print("What would you like to see?")
        print("[A] Appointments - see my appointment history")
        print("[M] Mood - view and delete my past mood entries")
        print("[J] Journal - view, edit and delete my past journal entries")
        print("[X] Exit")

        user_input = input("> ").strip().lower()
        if check_exit(user_input):
            return
        match user_input:
            case 'a':
                show_appointment_history(user)
            case 'm':
                show_mood_history(user, auth_service)
            case 'j':
                show_journal_history(user, auth_service)
            case '_':
                print_system_message('Invalid input. Please try again.')
                time.sleep(1)


