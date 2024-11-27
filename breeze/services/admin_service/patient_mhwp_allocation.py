from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.utils.cli_utils import check_exit, check_previous, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import ADMIN_BANNER_STRING
from breeze.utils.print_patinet_utils import _print_users


def allocate_patient_to_mhwp(auth_service):
    """
    Allocates an unassigned patient to an available MHWP.

    Args:
        auth_service (AuthService): The authentication service managing user data.
    """
    while True:
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print_system_message("Allocate Patient to MHWP")

        unassigned_patients = []
        available_mhwps = []

        # Find unassigned patients and available MHWPs
        for user in auth_service.users.values():
            if isinstance(user, Patient) and not user.get_assigned_mhwp():
                unassigned_patients.append(user)
            elif isinstance(user, MHWP) and len(user.get_assigned_patients()) < 5:
                available_mhwps.append(user)

        if not unassigned_patients:
            print_system_message("No unassigned patients available. All patients assigned.")
            direct_to_dashboard()
            return

        # List of unassigned patients
        _print_users(unassigned_patients, "Unassigned Patients", show_assigned_patients=False)
        print("\nEnter the username of the unassigned patient to assign (or enter [X] to exit):")

        # Admin enters username of unassigned patient
        while True:
            selected_patient_username = input("> ").strip()

            if check_exit(selected_patient_username):
                return

            selected_patient = auth_service.users.get(selected_patient_username)
            if selected_patient and isinstance(selected_patient, Patient) and not selected_patient.get_assigned_mhwp():
                break
            else:
                print_system_message("Invalid username or patient is already assigned. Please enter a valid unassigned patient username.")

        # List of MHWPs
        if not available_mhwps:
            print_system_message("No available MHWPs at this moment. All MHWPs have reached their maximum capacity of 5 patients.")
            direct_to_dashboard()
            return

        clear_screen()
        print(ADMIN_BANNER_STRING)
        print(f"\nAssigning patient: {selected_patient.get_first_name()} {selected_patient.get_last_name()} (Username: {selected_patient.get_username()})")
        _print_users(available_mhwps, "Available MHWPs", show_assigned_patients=True)

        while True:
            selected_mhwp_username = input("\nEnter the username of the MHWP to assign the patient to (or enter [R] to return to previous menu): ").strip()

            if check_previous(selected_mhwp_username):
                break

            selected_mhwp = auth_service.users.get(selected_mhwp_username)
            if selected_mhwp and isinstance(selected_mhwp, MHWP):
                if len(selected_mhwp.get_assigned_patients()) < 5:
                    selected_patient.set_assigned_mhwp(selected_mhwp_username)
                    selected_mhwp.add_patient(selected_patient_username)

                    auth_service.save_data_to_file()

                    clear_screen()
                    print(ADMIN_BANNER_STRING)
                    print_system_message(f"Successfully assigned patient '{selected_patient.get_username()}' to MHWP '{selected_mhwp.get_username()}'.")
                    break
                else:
                    print_system_message(f"MHWP '{selected_mhwp.get_username()}' has already reached the maximum number of 5 patients. Please select a different MHWP.")
            else:
                print_system_message("Invalid MHWP username. Please enter a valid MHWP username.")