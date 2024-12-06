from datetime import datetime
from breeze.models.patient import Patient
from breeze.utils.cli_utils import (
    check_exit,
    check_previous,
    clear_screen_and_show_banner,
    direct_to_dashboard,
    print_system_message,
)
from breeze.utils.constants import MHWP_BANNER_STRING
from breeze.utils.mood_chart_utils import plot_mood_chart


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
        print("-" * 125)
        print(
            f"| {'Username':<15} | {'First Name':<15} | {'Last Name':<15} | {'Gender':<10} | {'DOB':<13} | {'Condition':<20} | {'Medication':<15} |"
        )
        print("-" * 125)
        for patient in patients:
            # Get the most recent condition and prescription if there are multiple ones
            conditions = patient.get_conditions()
            if conditions:
                recent_condition = max(
                    conditions.items(),
                    key=lambda item: max(entry["timestamp"] for entry in item[1]),
                )
                condition_name = recent_condition[0]
            else:
                condition_name = "N/A"

            prescriptions = patient.to_dict()["prescriptions"]
            if prescriptions:
                recent_prescription = max(
                    prescriptions,
                    key=lambda p: datetime.strptime(p["start_date"], "%d-%m-%Y"),
                )
                medication_name = recent_prescription["medication"]
            else:
                medication_name = "N/A"

            print(
                f"| {patient.get_username():<15} | "
                f"{patient.get_first_name() or 'N/A':<15} | "
                f"{patient.get_last_name() or 'N/A':<15} | "
                f"{patient.get_gender() or 'N/A':<10} | "
                f"{patient.get_date_of_birth() or 'N/A':<13} | "
                f"{condition_name or 'N/A':<20} | "
                f"{medication_name or 'N/A':<15} |"
            )
        print("-" * 125)

    def show_patient_details(patient):
        """Displays detailed information for a selected patient."""
        clear_screen_and_show_banner(MHWP_BANNER_STRING)
        print_system_message(f"Details for {selected_patient.get_username()}:")
        print(
            f"Full Name: {selected_patient.get_first_name()} {selected_patient.get_last_name()}"
        )
        print(f"Gender: {selected_patient.get_gender()}")
        print(f"Date of Birth: {selected_patient.get_date_of_birth()}")

        print("\nConditions:")
        for condition, notes in selected_patient.get_conditions().items():
            print(f"  - {condition}:")
            for note in notes:
                print(f"    - {note['note']} (Added on: {note['timestamp']})")

        print("\nAppointment History:")
        appointments = patient.get_appointments()
        if appointments:
            print("-" * 50)
            print(f"| {'Date':<15} | {'Time':<10} | {'Status':<15} |")
            print("-" * 50)
            for appointment in appointments:
                print(
                    f"| {appointment.get_date().strftime('%d-%m-%Y'):<15} | "
                    f"{appointment.get_time().strftime('%I:%M %p'):<10} | "
                    f"{appointment.get_status():<15} | "
                )
            print("-" * 50)
        else:
            print("  No appointment history available.")

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

        mood_entries = patient.get_mood_entries()
        if mood_entries:
            plot_mood_chart(mood_entries)
        else:
            print("  No mood records available.")

        navigation = input("\nEnter [R] to return to the patient summary.\n >")

        if check_previous(navigation):
            clear_screen_and_show_banner(MHWP_BANNER_STRING)
            show_assigned_patients_table(assigned_patients)

    # Main Summary Logic
    clear_screen_and_show_banner(MHWP_BANNER_STRING)

    all_users = auth_service.get_all_users()
    assigned_patients = [
        patient
        for patient in all_users.values()
        if isinstance(patient, Patient)
        and patient.get_assigned_mhwp() == user.get_username()
    ]

    if not assigned_patients:
        print_system_message("No patients are currently assigned to you.")
        direct_to_dashboard()
        return

    show_assigned_patients_table(assigned_patients)

    while True:

        print(
            "\nEnter the username of the patient to view details (or press [X] to exit):"
        )
        selected_username = input("> ").strip().lower()
        if check_exit(selected_username):
            break

        selected_patient = next(
            (
                patient
                for patient in assigned_patients
                if patient.get_username() == selected_username
            ),
            None,
        )
        if selected_patient:
            show_patient_details(selected_patient)
        else:
            print_system_message("Invalid username. Please try again.")
