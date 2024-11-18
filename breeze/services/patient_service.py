from breeze.utils.cli_utils import print_system_message, clear_screen, direct_to_dashboard, return_to_previous, show_disabled_account_dashboard_menu
from breeze.utils.constants import PATIENT_BANNER_STRING
from breeze.utils.data_utils import load_data, save_data
import datetime
import time


class PatientService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def show_patient_dashboard(self, user):
        """Displays the patient dashboard and processes user actions.

        Args:
            user (User): _The logged-in user

        Returns:
            bool: True if the user chose to log out, otherwise False
        """
        
        print(PATIENT_BANNER_STRING)
        
        if user.get_is_disabled():
            return show_disabled_account_dashboard_menu(user.get_username())
             
        else:
            # If account is not disabled, show the full list of options
            print('Hi', user.get_username(), '!')
            print('What do you want to do today?')
            print("[E] Edit my personal information")
            print("[R] Record my mood for today")
            print("[J] Journal - enter your journaling text")
            print("[S] Search for meditation and relaxation exercises")
            print("[B] Book or cancel an appointment with my MHWP")
            print("[X] Log out")

            user_input = input('> ')
            match user_input.strip().lower():
                case "e":
                    self.edit_personal_information(user)
                case "r":
                    self.record_mood(user)
                case "j":
                    self.enter_journaling(user)
                case "s":
                    self.search_exercise(user)
                case "x":
                    return True
                case _:
                    print_system_message("Invalid choice. Please try again.")

        return False

    def edit_personal_information(self, user):
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f'Hi {user.get_first_name()} (username: {user.get_username()}) ! Please update your personal information')
        print('Here is your current information:')
        print_system_message(f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}")
        
        print("\nEnter the new information or leave blank to keep the current value:")
        # get user input and update that user info
        updated_first_name = input("First name: ").strip()
        updated_last_name = input("Last name: ").strip()
        updated_email = input("email: ").strip()
        updated_emergency_contact_email = input("emergency contact email: ").strip()
        
        # TODO: validate the inputs
        if updated_first_name:
            user.set_first_name(updated_first_name)
        if updated_last_name:
            user.set_last_name(updated_last_name)
        if updated_email:
            user.set_email(updated_email)
        if updated_emergency_contact_email:
            user.set_emergency_contact(updated_emergency_contact_email)
        
        # set the update message based on whether the user update all the fields or not
        update_message = ""
        if not updated_first_name and not updated_last_name and not updated_email and not updated_emergency_contact_email:
            update_message = "\nHere is your updated information (no changes made):"
        else:
            update_message = '\nInfo updated successfully! Here is your updated information:'
        
        print(update_message)
        print_system_message(f"First name: {user.get_first_name()}\nLast name: {user.get_last_name()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}")
        
        # Save the changes to the file via AuthService
        self.auth_service.save_data_to_file()
        
        direct_to_dashboard()
    
    def record_mood(self, user):
        clear_screen()
        print(PATIENT_BANNER_STRING)
        
        print("Record Your Mood for the Day")
        print("Please choose a colour that best describes your mood:")
        print("[G]reen - Very Happy")
        print("[L]ight Green - Happy")
        print("[Y]ellow - Neutral")
        print("[O]range - Sad")
        print("[R]ed - Very Sad")

        colour_to_mood = {
            "g": "Very Happy",
            "l": "Happy",
            "y": "Neutral",
            "o": "Sad",
            "r": "Very Sad"
        }

        while True:
            colour_input = input("Enter the colour code that represents your mood today: ").strip().lower()
            if colour_input in colour_to_mood:
                mood_description = colour_to_mood[colour_input]
                comment = input("Would you like to add any additional comments about your mood today? Type [R] to discard your entry: ").strip()
                
                if comment.lower() == 'r':
                    print_system_message("Mood entry discarded. Returning to dashboard.")
                    direct_to_dashboard()
                    return

                date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mood_entry = {
                    "mood": mood_description,
                    "comment": comment,
                    "datetime": date_string
                }

                if hasattr(user, "add_mood_entry"):
                    user.add_mood_entry(mood_description, comment, date_string)

                self.auth_service.save_data_to_file()

                print_system_message("Mood recorded successfully!")
                direct_to_dashboard()  
                return
            else:
                print_system_message("Invalid colour entered. Please choose from Green, Light Green, Yellow, Orange, or Red.")

    def enter_journaling(self, user):
        # Include util 'print system message'
        # Include all funcs from data utils to load/save entry to json file
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f'Hi {user.get_username()} !')
        print_system_message('Write your journal entry below, or enter [R] at any time to return to the previous page without saving')
        journal_title = input('What is the title of your entry? \n').strip()
        if return_to_previous(journal_title, 'r'):
            return
        if journal_title.strip() == '':
            print_system_message('Your title is empty! Returning to dashboard...')
            time.sleep(2)
            return
        journal_body = input('Write your journal entry here: \n').strip()
        if return_to_previous(journal_body, 'r'):
            return
        journal_additions = []
        in_progress = True
        while in_progress:
            journal_addition = input('Would you like to write more? Type [N] if finished, or continue writing: \n').strip()
            if return_to_previous(journal_addition, 'r'):
                return
            if journal_addition.lower() == 'n':
                in_progress = False
            else:
                journal_additions.append(journal_addition)
                clear_screen()
                print(PATIENT_BANNER_STRING)
                print('Write your journal entry below, or enter [R] at any time to return to the previous page without saving: \n')
                print(journal_title)
                print(journal_body)
                print("\n".join(journal_additions))

        journal_ent = (journal_body + ' ' + ' '.join(journal_additions))
        if journal_ent.strip() == '':
            print_system_message('Entry is empty! Returning to dashboard...')
            time.sleep(2)
            return

        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {'title' : journal_title, 'text': journal_ent, 'date' : date_string}
        if hasattr(user, "add_journal_entry"):
            # save file to users.json
            user.add_journal_entry(journal_title, journal_ent, date_string)
            self.auth_service.save_data_to_file()
            print_system_message('Journal entry saved! Returning to dashboard...')
            time.sleep(2)
            return
        print_system_message(f'User {user} not in records!')
        time.sleep(2)
        return

    def search_exercise(self, user):
        """Allows the patient to search for meditation and relaxation exercises by keyword."""
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print_system_message("Search for Meditation and Relaxation Exercises")
        
        valid_keywords = {
            "sleep": "deep-sleep",
            "piano": "piano-meditation",
            "rain": "rain-and-thunder-sound-therapy",
            "campfire": "nature-sounds-campfire-and-stream",
            "harp": "i-see-you-harp"
        }
        
        print_system_message("Choose a sound you like from the following options:")
        for keyword in valid_keywords.keys():
            print(f"- {keyword.capitalize()}")
        
        while True:
            print()
            keyword = input("Enter a keyword from the list above to start your meditation: ").strip().lower()
            
            if keyword in valid_keywords:
                search_url = f"https://insighttimer.com/indiemusicbox/guided-meditations/{valid_keywords[keyword]}"
                print_system_message(f"Here is your selected meditation for '{keyword}':")
                print(search_url)
                break
            else:
                print_system_message("Invalid keyword. Please choose a keyword from the list.")

        direct_to_dashboard()
            
    def manage_appointment(self, user):
        pass
        
