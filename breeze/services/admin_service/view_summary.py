from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.utils.cli_utils import clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import ADMIN_BANNER_STRING


def view_summary(auth_service):
    """
    Displays a summary of admin-related information.
    """
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("User Summary")
    
    # Fetch all users
    users = auth_service.get_all_users().values()
    
    # Separate patients and MHWPs
    patients = [user for user in users if isinstance(user, Patient)]
    mhwps = [user for user in users if isinstance(user, MHWP)]

    print("\nPatients Summary:")
    print("-" * 101)
    print(f"| {'Username':<15} | {'First Name':<15} | {'Last Name':<15} | {'Email':<25} | {'Assigned MHWP':<15} |")
    print("-" * 101)
    for patient in patients:
        print(
            f"| {patient.get_username():<15} | "
            f"{patient.get_first_name() or 'N/A':<15} | "
            f"{patient.get_last_name() or 'N/A':<15} | "
            f"{patient.get_email() or 'N/A':<25} | "
            f"{patient.get_assigned_mhwp() or 'Unassigned':<15} |"
        )
    print("-" * 101)

    print("\nMHWP Summary:")
    print("-" * 124)
    print(f"| {'Username':<15} | {'First Name':<15} | {'Last Name':<15} | {'Email':<25} | {'Assigned Patients':<17} | {'Confirmed Bookings':<18} |")
    print("-" * 124)
    for mhwp in mhwps:
        assigned_patients = len(mhwp.get_assigned_patients()) if mhwp.get_assigned_patients() else 0
        confirmed_bookings = sum(
            1 for appointment in mhwp.get_appointments() if appointment.get_status() == "confirmed"
        )
        print(
            f"| {mhwp.get_username():<15} | "
            f"{mhwp.get_first_name() or 'N/A':<15} | "
            f"{mhwp.get_last_name() or 'N/A':<15} | "
            f"{mhwp.get_email() or 'N/A':<25} | "
            f"{assigned_patients:<17} | "
            f"{confirmed_bookings:<18} |"
        )
    
    print("-" * 124)
    direct_to_dashboard()