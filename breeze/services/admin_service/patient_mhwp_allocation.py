from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.services.admin_service.admin_user_printer import print_users
from breeze.utils.cli_utils import check_exit, check_previous, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import ADMIN_BANNER_STRING
                
def reallocate_patient_to_mhwp(auth_service):
    while True:
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print_system_message("Reallocate Patient to MHWP")

        patients = [user for user in auth_service.users.values() if isinstance(user, Patient)]
        mhwps = [user for user in auth_service.users.values() if isinstance(user, MHWP)]

        if not patients:
            print_system_message("No patients found.")
            direct_to_dashboard()
            return

        print_users(patients, "List of All Patients and Their Assigned MHWPs:", show_assigned_patients=False)
        print("\nEnter the username of the patient to reallocate (or enter [X] to exit):")
        
        while True:
            selected_patient_username = input("> ").strip().lower()

            if check_exit(selected_patient_username):
                return

            selected_patient = auth_service.users.get(selected_patient_username)
            if selected_patient and isinstance(selected_patient, Patient):
                break
            else:
                print_system_message("Invalid username. Please enter a valid patient username.")
                
            # List of MHWPs
        clear_screen()
        print(ADMIN_BANNER_STRING)
        assigned_mhwp_username = selected_patient.get_assigned_mhwp()

        if assigned_mhwp_username:
            assigned_mhwp = auth_service.get_user_by_username(assigned_mhwp_username)
            mhwp_name = f"{assigned_mhwp.get_first_name()} {assigned_mhwp.get_last_name()} (Username: {assigned_mhwp.get_username()})"
        else:
            mhwp_name = "Unassigned"
            
        print(f"\nPatient: {selected_patient.get_first_name()} {selected_patient.get_last_name()} (Username: {selected_patient.get_username()}) is currently assigned to: {mhwp_name}")
        print_users(mhwps, "Available MHWPs", show_assigned_patients=True)
            
        
        while True:
            selected_mhwp_username = input("\nEnter the username of the MHWP to allocate the patient to (or enter [R] to return to previous menu): ").strip()
            
            if check_previous(selected_mhwp_username):
                break

            selected_mhwp = auth_service.users.get(selected_mhwp_username)
            if selected_mhwp and isinstance(selected_mhwp, MHWP):
                if assigned_mhwp_username == selected_mhwp_username:
                    clear_screen()
                    print(ADMIN_BANNER_STRING)
                    print_system_message(f"This patient is already allocated to MHWP '{selected_mhwp.get_first_name()} {selected_mhwp.get_last_name()}'. No changes were required.")
                    direct_to_dashboard("No changes required!")
                    return
                else:
                    if assigned_mhwp_username:
                        previous_mhwp = auth_service.users.get(assigned_mhwp_username)
                        if previous_mhwp and isinstance(previous_mhwp, MHWP):
                            previous_mhwp.get_assigned_patients().remove(selected_patient.get_username())
                    
                    selected_patient.set_assigned_mhwp(selected_mhwp_username)
                    selected_mhwp.add_patient(selected_patient_username)

                    auth_service.save_data_to_file()

                    clear_screen()
                    print(ADMIN_BANNER_STRING)
                    print_system_message(f"Successfully reallocated patient '{selected_patient.get_username()}' to MHWP '{selected_mhwp.get_username()}'.")
                    direct_to_dashboard("Patient allocation saved!")
                    return
            else:
                print_system_message("Invalid MHWP username. Please enter a valid MHWP username.")