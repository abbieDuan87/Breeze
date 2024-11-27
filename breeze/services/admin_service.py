from breeze.utils.cli_utils import check_exit, print_system_message, clear_screen, direct_to_dashboard
from breeze.utils.constants import ADMIN_BANNER_STRING
from breeze.models.patient import Patient
from breeze.models.mhwp import  MHWP



class AdminService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def show_admin_dashboard(self, user):
        """
        Displays the admin dashboard and processes user actions.

        Args:
            user (User): _The logged-in user
            
        Returns:
            bool: True if the user chose to log out, otherwise False
        """
        while True:
            clear_screen()
            print(ADMIN_BANNER_STRING)
            print('Hi', user.get_username(), '!')
            print('What do you want to do today?')
            print('[R] Reallocate patient to MHWP')
            print('[E] Edit user information')
            print('[D] Delete a user')
            print('[I] Disable a user')
            print('[V] View summary')
            print('[X] Log out')

            user_input = input("> ").strip().lower()

            if user_input in ["r", "e", "d", "i", "v", "x"]: 
                match user_input:
                    case "r":
                        self.reallocate_patient_to_mhwp()
                    case "e":
                        self.edit_user_information()
                    case "d":
                        self.delete_user(user)
                    case "i":
                        self.disable_user(user)
                    case "v":
                        self.view_summary()
                    case "x":
                        return True

    def reallocate_patient_to_mhwp(self):
        while True:
            clear_screen()
            print(ADMIN_BANNER_STRING)
            print_system_message("Reallocate Patient to MHWP")

            patients = []
            mhwps = []

        # Find unassigned patients and available MHWPs
            for username, user in self.auth_service.users.items():
                if isinstance(user, Patient):
                    patients.append(user)
                elif isinstance(user, MHWP):
                    mhwps.append(user)
                
            if not patients:
                print_system_message("No patients found.")
                direct_to_dashboard()
                return
                
            # List of all patients and default MHWP assignment
            print("List of all Patients and their assigned MHWP:")
            print("-" * 83)
            print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} | {'Assigned MHWP':<20} |")
            print("-" * 83)

            for patient in patients:
                username = patient.get_username()
                first_name = patient.get_first_name() or "N/A"
                last_name = patient.get_last_name() or "N/A"
                assigned_MHWP = patient.get_assigned_mhwp() or "Unassigned"
                print(f"| {username:<20} | {first_name:<15} | {last_name:<15} | {assigned_MHWP:<20} |")
            print("-" * 83)
    
            print("\nEnter the username of the patient to reallocate (or enter [X] to return to the dashboard):")
            # Admin enters username of patient
            while True:
                selected_patient_username = input("> ").strip()

                if check_exit(selected_patient_username):
                    return

                selected_patient = self.auth_service.users.get(selected_patient_username)
                if selected_patient and isinstance(selected_patient, Patient):
                    break
                else:
                    print_system_message("Invalid username. Please enter a valid unassigned patient username.")
                    
                # List of MHWPs
            clear_screen()
            print(ADMIN_BANNER_STRING)
            assigned_mhwp_username = selected_patient.get_assigned_mhwp()

            if assigned_mhwp_username:
                assigned_mhwp = self.auth_service.get_user_by_username(assigned_mhwp_username)
                mhwp_name = f"{assigned_mhwp.get_first_name()} {assigned_mhwp.get_last_name()} (Username: {assigned_mhwp.get_username()})"
            else:
                mhwp_name = "Unassigned"
                
            print(f"\nPatient: {selected_patient.get_first_name()} {selected_patient.get_last_name()} (Username: {selected_patient.get_username()}) is currently assigned to: {mhwp_name}")
            self._print_users(mhwps, "MHWPs", show_assigned_patients=True)
                
            
            while True:
                selected_mhwp_username = input("\nEnter the username of the MHWP to allocate the patient to: ").strip()

                selected_mhwp = self.auth_service.users.get(selected_mhwp_username)
                if selected_mhwp and isinstance(selected_mhwp, MHWP):
                    if assigned_mhwp_username == selected_mhwp_username:
                        clear_screen()
                        print(ADMIN_BANNER_STRING)
                        print_system_message(f"This patient is already allocated to MHWP '{selected_mhwp.get_first_name()} {selected_mhwp.get_last_name()}'. No changes were required.")
                        direct_to_dashboard("No changes required!")
                        return
                    else:
                        if assigned_mhwp_username:
                            previous_mhwp = self.auth_service.users.get(assigned_mhwp_username)
                            if previous_mhwp and isinstance(previous_mhwp, MHWP):
                                previous_mhwp.get_assigned_patients().remove(selected_patient.get_username())
                        
                        selected_patient.set_assigned_mhwp(selected_mhwp_username)
                        selected_mhwp.add_patient(selected_patient_username)

                        self.auth_service.save_data_to_file()

                        clear_screen()
                        print(ADMIN_BANNER_STRING)
                        print_system_message(f"Successfully reallocated patient '{selected_patient.get_username()}' to MHWP '{selected_mhwp.get_username()}'.")
                        direct_to_dashboard("Patient allocation saved!")
                        return
                else:
                    print_system_message("Invalid MHWP username. Please enter a valid MHWP username.")


    def edit_user_information(self):
        """
        Allows admin to edit information for a patient or an MWHP
        """
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print_system_message("Edit User Information")

        while True:
            print("\nDo you want to edit information for a Patient or an MHWP?\nEnter [P] for Patient or [M] for MHWP (or [R] to return to the dashboard):")
            user_input = input("> ").strip().lower()

            if user_input == "r":
                return  
            elif user_input in ["p", "m"]:
                break
            else:
                print_system_message("Invalid choice.")

        # Filter and display users of the chosen type
        users_to_edit = []
        if user_input == "p":
            users_to_edit = [user for user in self.auth_service.users.values() if isinstance(user, Patient)]
            title = "Patients"
        elif user_input == "m":
            users_to_edit = [user for user in self.auth_service.users.values() if isinstance(user, MHWP)]
            title = "MHWPs"

        # Display table of users
        clear_screen()
        print(ADMIN_BANNER_STRING)
        self._print_users(users_to_edit, title, show_assigned_patients=False)
       
        while True:
            print("\nEnter the username of the user to edit (or enter [R] to return to the dashboard):")
            username = input("> ").strip()

            if username.lower() == "r":
                return

            if not username:
                print_system_message("Username cannot be empty. Please enter a valid username.\n")
                continue

            user = self.auth_service.users.get(username)

            if user:
                clear_screen()
                print(ADMIN_BANNER_STRING)
                print(f"Editing information for user: {user.get_username()}")
                print('Here is the current information:')
                current_info = (
                    f"First name: {user.get_first_name()}\n"
                    f"Last name: {user.get_last_name()}\n"
                    f"Email: {user.get_email()}\n"
                )

                if isinstance(user, Patient):
                    current_info += f"Emergency contact email: {user.get_emergency_contact()}\n"

                print_system_message(current_info)


                print("\nEnter the new information or leave blank to keep the current value:")
            # get user input and update that user info
                updated_first_name = input("First name: ").strip()
                updated_last_name = input("Last name: ").strip()
                updated_email = input("Email: ").strip()
                updated_emergency_contact_email = None

                if isinstance(user, Patient):
                    updated_emergency_contact_email = input("Emergency contact email: ").strip()
            
            # TODO: validate the inputs
                if updated_first_name:
                    user.set_first_name(updated_first_name)
                if updated_last_name:
                    user.set_last_name(updated_last_name)
                if updated_email:
                    user.set_email(updated_email)
                if updated_emergency_contact_email:
                    user.set_emergency_contact(updated_emergency_contact_email)
            
                update_message = ""
                if not updated_first_name and not updated_last_name and not updated_email and not updated_emergency_contact_email:
                    update_message = "\nHere is your updated information (no changes made):"

                else:
                    update_message = '\nInfo updated successfully! Here is your updated information:'
                
                clear_screen()
                print(ADMIN_BANNER_STRING)
                print(update_message)
                # added str just in case there are any type errors
                updated_info = (
                "First name: " + str(user.get_first_name()) + "\n"
                "Last name: " + str(user.get_last_name()) + "\n"
                "Email: " + str(user.get_email()) + "\n"
                )

                if isinstance(user, Patient):
                    updated_info = updated_info + "Emergency contact email: " + str(user.get_emergency_contact()) + "\n"
            
                print_system_message(updated_info)

                self.auth_service.users[username] = user
                self.auth_service.save_data_to_file()

                direct_to_dashboard()
                return
                
            else:
                print_system_message("User not found. Please enter a valid username.")
                
        
               


    def delete_user(self,user):
        clear_screen()
        print(ADMIN_BANNER_STRING)
        
        print(f'Hi {user.get_username()} ! Here are all the users:')
        users = self.auth_service.get_all_users().values()
        print("-" * 42)  
        print(f"| {'Username':<20} | {'Role':<15} |")
        print("-" * 42) 
        for user in users:
            if not user.get_role() == 'Admin':
                username = user.get_username()
                role = user.get_role()
                print(f"| {username:<20} | {role:<15} |")
        print("-" * 42) 

       
        while True:
            print("Enter the username of the user you want to delete (case insensitive), or press [R] to cancel:")
            user_input = input("> ").strip().lower()
            
            if user_input == "r":
                break
            
            all_users = self.auth_service.get_all_users()
            user_to_delete = all_users.get(user_input)

            if not user_to_delete:
                print_system_message(f"Username '{user_input}' not found! Please try again")
            
            elif user_to_delete.get_role() == "Admin":
                print_system_message("You cannot delete admin accounts")
            
            else:
                print_system_message(f"Are you sure you want to delete the user '{user_input}'? Type [Y] to confirm or [N] to cancel")
                confirmation = input("> ").strip().lower()

                if confirmation == "y":
                    del all_users[user_input]
                    self.auth_service.save_data_to_file()
                    print_system_message(f"The user '{user_input}' has been sucessfully deleted")
                
                elif confirmation == "n":
                    print_system_message("Deletion cancelled. You can enter another username or press [R] to return")
                
                else:
                    print_system_message("Invalid input. Please type [Y] to confirm or [N] to cancel")        

        direct_to_dashboard()                



    def disable_user(self, user):
        clear_screen()
        print(ADMIN_BANNER_STRING)
        print(f'Hi {user.get_username()} ! Here are all the users:')
        self._print_users_with_disabled_status()
        
        while True:
            print("Enter the username of the account that you want to disable (case insensitive), or press [R] to cancel:")        
            user_input = input("> ").strip().lower()
            if user_input == "r":
                break
            elif not user_input in self.auth_service.get_all_users(): # TODO: not allow user with username r.
                print_system_message(f"Username '{user_input}' not found! Please try again")
            else:
                user_to_disable = self.auth_service.get_all_users().get(user_input) # get the user by username
                if user_to_disable.get_role() == "Admin":
                    print_system_message("You cannot disable this account.")
                elif user_to_disable.get_is_disabled(): 
                    print_system_message(f"The account '{user_input}' is already disabled.")
                else:  
                    user_to_disable.set_is_disabled(True) # disable the user
                    self.auth_service.save_data_to_file() # save the change
                    print_system_message(f"The account '{user_input}' has been successfully disabled.")
                
        direct_to_dashboard()
        
    def view_summary(self):
        pass

    def _print_users_with_disabled_status(self):
        """Private method that prints a list of all users and their account disabled status.
        
        This method is intended for AdminService class only and is responsible for displaying
        usernames, their roles, and whether their accounts are disabled. It excludes 
        users with the 'Admin' role from the list.

        Only the status of disabled accounts is shown for each user.

        Note:
            This is a private method and should not be accessed directly outside of 
            this class.
        """
        users = self.auth_service.get_all_users().values()
        
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

    
    def _print_users(self, users, title, show_assigned_patients=False):
        """Helper function to print the list of users in a table format.

        Args:
            users (list): List of users (Patients or MHWPs).
            title (str): Title for the table.
            show_assigned_patients (bool): Whether to show the 'Assigned Patients' column for MHWPs.
        """
        print(f"\n{title}:")
        
        if show_assigned_patients:
            print("-" * 83)
            print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} | {'Assigned Patients':<20} |")
            print("-" * 83)
        else:
            print("-" * 60)
            print(f"| {'Username':<20} | {'First Name':<15} | {'Last Name':<15} |")
            print("-" * 60)

        for user in users:
            username = user.get_username()
            first_name = user.get_first_name() or "N/A"
            last_name = user.get_last_name() or "N/A"
            
            if show_assigned_patients and isinstance(user, MHWP):
                assigned_patients = str(len(user.get_assigned_patients()))
                print(f"| {username:<20} | {first_name:<15} | {last_name:<15} | {assigned_patients:<20} |")
            else:
                print(f"| {username:<20} | {first_name:<15} | {last_name:<15} |")

        if show_assigned_patients:
            print("-" * 83)
        else:
            print("-" * 60)

