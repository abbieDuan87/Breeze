import time
from datetime import datetime
from breeze.utils.appointment_utils import (
    handle_appointment_action,
    show_upcoming_appointments,
)
from breeze.utils.cli_utils import (
    clear_screen_and_show_banner,
    print_system_message,
    clear_screen,
    direct_to_dashboard,
    show_disabled_account_dashboard_menu,
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

        while True:
            clear_screen()
            print(MHWP_BANNER_STRING)

            if user.get_is_disabled():
                return show_disabled_account_dashboard_menu(user.get_username())

            print(f"Hi", user.get_username(), "!")
            print("What do you want to do today?")
            print("[C] View Calendar of Appointments")
            print("[M] Manage Appointments (Confirm or Cancel)")
            print("[A] Add Patient Information (Condition, Notes)")
            print("[D] Display Patient Summary with Mood Chart")
            print("[X] Log out")

            user_input = input("> ").strip().lower()

            if user_input in ["c", "m", "a", "d", "x"]:
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
                

    def view_calendar(self, user):
        clear_screen_and_show_banner(MHWP_BANNER_STRING)
        user.display_calendar()
        print()

        direct_to_dashboard()

    def manage_appointments(self, user):
        def handle_action(upcoming_appointments, action, prompt):
            """Reusable logic to handle appointment actions (cancel or confirm)."""
            while True:
                clear_screen_and_show_banner(MHWP_BANNER_STRING)
                upcoming_appointments = show_upcoming_appointments(
                    user,
                    (
                        lambda app: (
                            app.get_date(),
                            app.get_time(),
                            app.patient_username,
                        )
                    ),
                )

                print(
                    f"\nEnter the index number of the appointment you want to {action} (or type [R] to return):"
                )
                selected_index_input = input("> ").strip().lower()

                if selected_index_input == "r":
                    break

                try:
                    selected_index = int(selected_index_input)

                    if not handle_appointment_action(
                        upcoming_appointments, selected_index, self.auth_service, action
                    ):
                        print_system_message("Action could not be completed.")

                except ValueError as ve:
                    if "invalid literal for int()" in str(ve):
                        print_system_message("Please enter a valid number.")
                    else:
                        print_system_message(str(ve))

                    time.sleep(0.5)
                    continue

        while True:
            clear_screen_and_show_banner(MHWP_BANNER_STRING)
            print(f"Hi, {user.get_username()} !")
            upcoming_appointments = show_upcoming_appointments(
                user,
                (lambda app: (app.get_date(), app.get_time(), app.patient_username)),
            )
            
            if not upcoming_appointments:
                time.sleep(1)
                break

            print("\nChoose one of the following options:")
            print("\n[C] Cancel appointments\n[F] Confirm appointments\n[E] Exit\n")

            selected_action = input("> ").strip().lower()

            if selected_action == "c":
                handle_action(upcoming_appointments, "cancel", "Cancel")
            elif selected_action == "f":
                handle_action(upcoming_appointments, "confirm", "Confirm")
            elif selected_action == "e":
                direct_to_dashboard()
                break
            else:
                print_system_message("Please enter a valid option.")
                time.sleep(0.5)

    def add_patient_information(self, user):
        def display_patient_menu(patients):                         #List of assigned patients
            print("-" * 42)
            print(f"| {'Username':<20} | {'Assigned MHWP':<15} |")
            print("-" * 42)
            for patient in patients:
                print(f"| {patient.get_username():<20} | {patient.get_assigned_mhwp():<15} |")
            print("-" * 42)

        def display_condition_menu(patient):                        #dislays the common conditions menu for mhwp to choose from
            print(MHWP_BANNER_STRING)
            print(f"Adding condition for patient: {patient.get_username()}")
            print("Choose a condition or enter a custom option:")
            print("[1] Anxiety")
            print("[2] Depression")
            print("[3] Stress")
            print("[4] PTSD (Post-Traumatic Stress Disorder)")
            print("[5] OCD (Obsessive-Compulsive Disorder)")
            print("[6] Bipolar Disorder")
            print("[7] Eating Disorders")
            print("[8] Phobias")
            print("[9] Panic disorder")
            print("[10] Antisocial personality disorder (ASPD)")
            print("[O] Other condition")
            print("[X] Exit")

        def get_condition_choice(patient):                          # Takes care of condition choice and errors
            predefined_conditions = {
                "1": "Anxiety",
                "2": "Depression",
                "3": "Stress",
                "4": "PTSD (Post-Traumatic Stress Disorder)",
                "5": "OCD (Obsessive-Compulsive Disorder)",
                "6": "Bipolar Disorder",
                "7": "Eating Disorders",
                "8": "Phobias",
                "9": "Panic disorder",
                "10": "Antisocial personality disorder (ASPD)"
            }
            display_condition_menu(patient)
            while True:
                choice = input("\nSelect a condition by entering a number, [O] for other condition and [X] to exit: ").strip().lower()

                if choice in predefined_conditions:
                    return predefined_conditions[choice]
                elif choice == "o":
                    return input("Enter the patient's custom condition: ").strip()
                elif choice == "x":
                    return 
                else:
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    display_condition_menu(patient)
                    print_system_message("Invalid choice. Please try again.")

        while True:
            clear_screen()
            print(MHWP_BANNER_STRING)
            print(f"Hi {user.get_username()}! Let's add patient information.")

            all_users = self.auth_service.get_all_users()

            # Patients assigned to the MHWP
            assigned_patients = [
                patient for patient in all_users.values()
                if isinstance(patient, Patient) and patient.get_assigned_mhwp() == user.get_username()
            ]

            if not assigned_patients:
                print_system_message("No patients are currently assigned to you.")
                direct_to_dashboard()
                return

            # Display assigned patients in a table format
            display_patient_menu(assigned_patients)

            # Select a patient
            while True:
                patient_username = input("\nEnter the patient's username to add information, or [X] to exit: ").strip().lower()
                if patient_username == "x":
                    return
                patient = next((p for p in assigned_patients if p.get_username() == patient_username), None)
                if patient:
                    break
                else:
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Hi {user.get_username()}! Let's add patient information.")
                    display_patient_menu(assigned_patients)
                    print_system_message("Invalid username. Please try again.")
                    

            # Options for adding condition/prescription or exiting
            clear_screen()
            print(MHWP_BANNER_STRING)
            print(f"Updating Patient: {patient.get_username()}")
            print("\nWhat would you like to do?")
            print("[C] Add a condition")
            print("[P] Add a prescription")
            print("[X] Exit")           
            while True:
                option = input("Enter your choice: ").strip().lower()

                if option == "c":
                    while True:
                        condition = get_condition_choice(patient)
                        if not condition:
                            break

                        print(f"Selected Condition: {condition}")
                        notes = input("Enter notes about the condition: ").strip()
                        patient.add_condition(condition, notes)
                        self.auth_service.save_data_to_file()
                        print_system_message(f"Condition '{condition}' with notes saved successfully.")
                        direct_to_dashboard()
                        return

                elif option == "p":
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Adding Prescription for Patient: {patient.get_username()}")
                    medication = input("\nMedication: ").strip()

                    # Ask for units for dosage
                    print("\nPlease select a unit for the medications dosage or enter a custom unit:")
                    predefined_units = ["mg", "ml", "tablets", "capsules", "drops"]
                    for i, unit in enumerate(predefined_units, 1):
                        print(f"[{i}] {unit}")
                    print("[O] Other")

                    while True:
                        unit_choice = input("\nSelect a unit by selecting a number or [O] for other: ").strip().lower()
                        if unit_choice.isdigit() and 1 <= int(unit_choice) <= len(predefined_units):
                            unit = predefined_units[int(unit_choice) - 1]
                            break
                        elif unit_choice == "o":
                            unit = input("Enter a custom unit: ").strip()
                            break
                        else:
                            clear_screen()
                            print(MHWP_BANNER_STRING)
                            print(f"Recorded Medication: {medication}")
                            print("\nnSelect a unit by number or [O] for other::")
                            predefined_units = ["mg", "ml", "tablets", "capsules", "drops"]
                            for i, unit in enumerate(predefined_units, 1):
                                print(f"[{i}] {unit}")
                            print("[O] Other")
                            print_system_message("Invalid unit selection. Please try again.")

                    # Ask for dosage
                    while True:
                        dosage = input(f"Enter dosage (in {unit}): ").strip()
                        if dosage.isnumeric() and float(dosage) > 0:
                            break
                        clear_screen()
                        print(MHWP_BANNER_STRING)
                        print(f"Recorded Medication: {medication}")
                        print_system_message("Invalid dosage. Please enter a positive number.")

                    frequency = input("Frequency (example: once daily): ").strip()

                    while True:
                        start_date = input("Start Date (DD-MM-YYYY): ").strip()
                        end_date = input("End Date (DD-MM-YYYY): ").strip()
                        try:
                            start = datetime.strptime(start_date, "%d-%m-%Y")
                            end = datetime.strptime(end_date, "%d-%m-%Y")
                            if start < end:
                                break
                            clear_screen()
                            print(MHWP_BANNER_STRING)
                            print_system_message("Start date must be before end date.")
                        except ValueError:
                            clear_screen()
                            print(MHWP_BANNER_STRING)
                            print_system_message("Invalid date format. Use DD-MM-YYYY.")

                    prescription_notes = input("Notes: ").strip()
                    patient.add_prescription(medication, f"{dosage} {unit}", frequency, start_date, end_date, prescription_notes)
                    self.auth_service.save_data_to_file()
                    print_system_message(f"Prescription '{medication}' added and saved successfully.")
                    direct_to_dashboard()
                    return

                elif option == "x":
                    return
                else:
                    clear_screen()
                    print(MHWP_BANNER_STRING)
                    print(f"Updating Patient: {patient.get_username()}")
                    print("\nWhat would you like to do?")
                    print("[C] Add a condition")
                    print("[P] Add a prescription")
                    print("[X] Exit")  
                    print_system_message("Invalid option. Please select [C], [P], or [X].")



    def display_patient_summary(self, user):
        pass
