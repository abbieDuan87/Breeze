from datetime import datetime
import matplotlib.pyplot as plt
from breeze.models.patient import Patient
from breeze.utils.cli_utils import clear_screen_and_show_banner, direct_to_dashboard, print_system_message
from breeze.utils.constants import MHWP_BANNER_STRING

def display_patient_summary(user, auth_service):
    """
    Displays a summary of all patients assigned to the MHWP, including mood charts.

    Args:
        user: The MHWP user.
        auth_service: The authentication service instance.
    """
    clear_screen_and_show_banner(MHWP_BANNER_STRING)
    
    def show_assigned_patients_table(patients):
        """Displays a table of assigned patients."""
        print("\nAssigned Patients:")
        print("-" * 110)
        print(f"| {'Username':<15} | {'First Name':<15} | {'Last Name':<15} | {'Condition':<25} | {'Medication':<30} |")
        print("-" * 110)
        for patient in patients:
            conditions = list(patient.get_conditions().keys())
            medications = [
                prescription["medication"]
                for prescription in patient.to_dict()["prescriptions"]
            ]
            print(
                f"| {patient.get_username():<15} | "
                f"{patient.get_first_name() or 'N/A':<15} | "
                f"{patient.get_last_name() or 'N/A':<15} | "
                f"{', '.join(conditions) or 'N/A':<25} | "
                f"{', '.join(medications) or 'N/A':<30} |"
            )
        print("-" * 110)

    def show_patient_details(patient):
        """Displays detailed information for a selected patient."""
        clear_screen_and_show_banner(MHWP_BANNER_STRING)
        print(f"Patient Details: {patient.get_first_name()} {patient.get_last_name()} (Username: {patient.get_username()})")

        # Appointment History
        print("\nAppointment History:")
        appointments = patient.get_appointments()
        if appointments:
            print("-" * 90)
            print(f"| {'Date':<15} | {'Time':<10} | {'Status':<15} | {'MHWP':<15} | {'Notes':<30} |")
            print("-" * 90)
            for appointment in appointments:
                print(
                    f"| {appointment.get_date().strftime('%Y-%m-%d'):<15} | "
                    f"{appointment.get_time().strftime('%I:%M %p'):<10} | "
                    f"{appointment.get_status():<15} | "
                    f"{appointment.mhwp_username or 'N/A':<15} | "
                    f"{appointment.get_notes() or 'N/A':<30} |"
                )
            print("-" * 90)
        else:
            print("  No appointment history available.")

        # Prescription Details
        print("\nPrescription Details:")
        prescriptions = patient.to_dict().get("prescriptions", [])
        if prescriptions:
            for prescription in prescriptions:
                print(f"  - Medication: {prescription['medication']}")
                print(f"    Dosage: {prescription['dosage']}")
                print(f"    Frequency: {prescription['frequency']}")
                print(f"    Start Date: {prescription['start_date']}")
                print(f"    End Date: {prescription['end_date']}")
                print(f"    Notes: {prescription.get('notes', 'N/A')}")
        else:
            print("  No prescriptions available.")

        # Mood Chart
        print("\nMood Chart")
        mood_entries = patient.get_mood_entries()
        if mood_entries:
            print("-" * 70)
            print(f"| {'Date':<25} | {'Mood':<15} | {'Comment':<25} |")
            print("-" * 70)
            for entry in mood_entries:
                print(
                    f"| {datetime.strptime(entry['datetime'], '%Y-%m-%d %H:%M:%S'):<25} | "
                    f"{entry['mood']:<15} | "
                    f"{entry.get('comment', 'N/A'):<25} |"
                )
            print("-" * 70)
        else:
            print("  No mood records available.")

        input("\nPress Enter to return to the patient list.")

    # Main Summary Logic
    clear_screen_and_show_banner(MHWP_BANNER_STRING)

    # Retrieve all users and filter patients assigned to the MHWP
    all_users = auth_service.get_all_users()
    assigned_patients = [
        patient for patient in all_users.values()
        if isinstance(patient, Patient) and patient.get_assigned_mhwp() == user.get_username()
    ]

    if not assigned_patients:
        print_system_message("No patients are currently assigned to you.")
        direct_to_dashboard()
        return

    # Display Table of Assigned Patients
    show_assigned_patients_table(assigned_patients)

    # Prompt User to Select a Patient for Detailed View
    while True:
        print("\nEnter the username of the patient to view details (or press [X] to exit):")
        selected_username = input("> ").strip().lower()
        if selected_username == "x":
            break

        selected_patient = next(
            (patient for patient in assigned_patients if patient.get_username() == selected_username),
            None,
        )
        if selected_patient:
            show_patient_details(selected_patient)
        else:
            print_system_message("Invalid username. Please try again.")

    direct_to_dashboard()