from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient


def print_users_with_disabled_status(auth_service):
        """Private method that prints a list of all users and their account disabled status.
        
        This method is intended for AdminService class only and is responsible for displaying
        usernames, their roles, and whether their accounts are disabled. It excludes 
        users with the 'Admin' role from the list.

        Only the status of disabled accounts is shown for each user.

        Note:
            This is a private method and should not be accessed directly outside of 
            this class.
        """
        users = auth_service.get_all_users().values()
        
        print("-" * 65)  
        print(f"| {'Username':<20} | {'Role':<15} | {'Is Account Disabled':<20} |")
        print("-" * 65)  

        # Print each user's details with vertical lines
        for user in users:
            if not user.get_role() == 'Admin':
                username = user.get_username()
                role = user.get_role()
                is_account_disabled = "True" if user.get_is_disabled() else "False"
                print(f"| {username:<20} | {role:<15} | {is_account_disabled:<20} |")
        
        print("-" * 65)

    
def print_users(users, title, show_assigned_patients=False, basic_view=False):
    """Helper function to print the list of users in a table format.

    Args:
        users (list): List of users (Patients or MHWPs).
        title (str): Title for the table.
        show_assigned_patients (bool): Whether to show the 'Assigned Patients' column for MHWPs or 'Assigned MHWP' for Patients.
        basic_view (bool): If True, only display username, first name, and last name.
    """
    print(f"\n{title}:")
    
    if basic_view:
        # Basic view: only username, first name, and last name
        print("-" * 60)
        print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} |")
        print("-" * 60)
    elif show_assigned_patients:
        # For MHWPs, show the assigned patients column
        print("-" * 83)
        print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} | {'Assigned Patients':<20} |")
        print("-" * 83)
    else:
        # For Patients, show the assigned MHWP column
        print("-" * 83)
        print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} | {'Assigned MHWP':<20} |")
        print("-" * 83)

    for user in users:
        username = user.get_username()
        first_name = user.get_first_name() or "N/A"
        last_name = user.get_last_name() or "N/A"
        
        if basic_view:
            # Basic view row
            print(f"| {username:<20} | {first_name:<15} | {last_name:<15} |")
        elif show_assigned_patients and isinstance(user, MHWP):
            # For MHWPs, count assigned patients
            assigned_patients = str(len(user.get_assigned_patients()))
            print(f"| {username:<20} | {first_name:<15} | {last_name:<15} | {assigned_patients:<20} |")
        elif not show_assigned_patients and isinstance(user, Patient):
            # For Patients, show the assigned MHWP
            assigned_mhwp = user.get_assigned_mhwp() or "Unassigned"
            print(f"| {username:<20} | {first_name:<15} | {last_name:<15} | {assigned_mhwp:<20} |")
        else:
            # Default row for any other user type (fallback)
            print(f"| {username:<20} | {first_name:<15} | {last_name:<15} |")

    if basic_view:
        print("-" * 60)
    else:
        print("-" * 83)