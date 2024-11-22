from breeze.utils.cli_utils import (
    print_system_message,
    clear_screen,
    direct_to_dashboard,
    show_disabled_account_dashboard_menu
)
from breeze.utils.constants import MHWP_BANNER_STRING
from breeze.models.patient import Patient


class MHWPService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def show_mhwp_dashboard(self, user):
        """
        Displays the MWHP dashboard and processes user actions.

        Args:
            user (User): _The logged-in user

        Returns:
            bool: True if the user chose to log out, otherwise False
        """

        print(MHWP_BANNER_STRING)

        if user.get_is_disabled():
            return show_disabled_account_dashboard_menu(user.get_username())

        else:
            print("Hi", user.get_username(), "!")
            print("What do you want to do today?")
            print("[C] View Calendar of Appointments")
            print("[M] Manage Appointments (Confirm or Cancel)")
            print("[A] Add Patient Information (Condition, Notes)")
            print("[D] Display Patient Summary with Mood Chart")
            print("[X] Log out")

            user_input = input("> ").strip().lower()
            match user_input:
                case "c":
                    self.view_calendar(user)
                case "m":
                    self.manage_appointments(user)
                case "a":
                    self.add_patient_information(user)
                case "d":
                    self.display_patient_summary(user)
                case "x":
                    return True
                case _:
                    print_system_message("Invalid choice. Please try again.")

        return False

    def view_calendar(self, user):
        clear_screen()
        print(MHWP_BANNER_STRING)
        user.display_calendar()
        print()

        direct_to_dashboard()

    def manage_appointments(self, user):
        pass

    def add_patient_information(self, user):
        while True:
            clear_screen()
            print(MHWP_BANNER_STRING)
            print(f"Hi {user.get_username()}! Let's add patient information.")

            all_users = self.auth_service.get_all_users()

            #patients assigned to the MHWP
            assigned_patients = [
                patient for patient in all_users.values()
                if isinstance(patient, Patient) and patient.get_assigned_mhwp() == user.get_username()
            ]

            if not assigned_patients:
                print_system_message("No patients are currently assigned to you.")
                direct_to_dashboard()
                return

            #display assigned patients
            print("Assigned Patients:")
            for patient in assigned_patients:
                print(f"- {patient.get_username()}")

            #select a patient
            while True:
                patient_username = input("\nEnter the patient's username to add information, or [R] to return: ").strip().lower()
                if patient_username == "r":
                    direct_to_dashboard()
                    return
                patient = next((p for p in assigned_patients if p.get_username() == patient_username), None)
                if patient:
                    break
                else:
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Hi {user.get_username()}! Let's add patient information.")
                    print("Assigned Patients:")
                    for patient in assigned_patients:
                        print(f"- {patient.get_username()}")
                    print_system_message("Invalid username. Please select from the list of assigned patients.")

            #Options for adding condition/prescription or returning
            while True:
                clear_screen()
                print(MHWP_BANNER_STRING)
                print(f"Updating Patient: {patient.get_username()}")
                print("\nWhat would you like to do?")
                print("[C] Add a condition")
                print("[P] Add a prescription")
                print("[R] Return to dashboard")
                option = input("Enter your choice: ").strip().lower()

                if option == "c":
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Adding condition for patient: {patient.get_username()}")
                    condition = input("\nEnter the patient's condition: ").strip()
                    notes = input("Enter notes about the condition: ").strip()
                    
                    patient.add_condition(condition, notes)
                    
                    self.auth_service.save_data_to_file()
                    print_system_message(f"Condition '{condition}' added and saved successfully.")
                    direct_to_dashboard()

                elif option == "p":
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Adding Prescription for Patient: {patient.get_username()}")
                    medication = input("\nMedication: ").strip()
                    dosage = input("Dosage: ").strip()
                    frequency = input("Frequency: ").strip()
                    start_date = input("Start Date (DD-MM-YYYY): ").strip()
                    end_date = input("End Date (DD-MM-YYYY): ").strip()
                    prescription_notes = input("Notes: ").strip()
                    
                    patient.add_prescription(medication, dosage, frequency, start_date, end_date, prescription_notes)
                    
                    self.auth_service.save_data_to_file()
                    print_system_message(f"Prescription '{medication}' added and saved successfully.")
                    direct_to_dashboard()

                elif option == "r":
                    direct_to_dashboard()
                    return
                else:
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print_system_message("Invalid option. Please select [C], [P], or [R].")


    def display_patient_summary(self, user):
        pass
