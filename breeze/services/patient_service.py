from breeze.utils.cli_utils import print_system_message, clear_screen
from breeze.utils.constants import PATIENT_BANNER_STRING

class PatientService:
    def __init__(self):
        pass
    
    def show_patient_dashboard(self, user):
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print('Hi', user.get_username(), '!')
        print('What do you want to do today?')
        
        print("[E] Edit my personal information")
        print("[R] Record my mood for today")
        print("[J] Journal - enter your journaling text")
        print("[S] Search for meditation and relaxation exercises")
        print("[B] Book or cancel an appointment with my MHWP")
        
        user_input = input('> ')
        match user_input.strip().lower():
            case "e":
                self.edit_personal_information(user)
            case _:
                print('end')
    
    def edit_personal_information(self, user):
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print(f'Hi {user.get_username()} ! Please update your personal information')
        print('Here is your current information:')
        print_system_message(f"name: {user.get_username()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}")
        
        print("\nEnter the new information or leave blank to keep the current value:")
        # get user input and update that user info
        updated_name = input("name: ").strip()
        updated_email = input("email: ").strip()
        updated_emergency_contact_email = input("emergency contact email: ").strip()
        
        # TODO: validate the inputs
        if updated_name:
            user.set_username(updated_name)
        if updated_email:
            user.set_email(updated_email)
        if updated_emergency_contact_email:
            user.set_emergency_contact(updated_emergency_contact_email)
        
        print('\nInfo updated successfully! Here is your updated information:')
        print_system_message(f"name: {user.get_username()}\nemail: {user.get_email()}\nemergency contact email: {user.get_emergency_contact()}")
        
        print("\nPress B to go back:")
        while True:
            user_input = input("> ").strip().lower()
            if user_input == "b":
                self.show_patient_dashboard(user)
                break
            else:
                print_system_message("Invalid input. Please press B to go back.")
        
    
    def record_mood(self, user):
        pass
    
    def enter_journaling(self, user):
        pass
    
    def search_exercise(self, user):
        pass
    
    def manage_appointment(self, user):
        pass
        
        
