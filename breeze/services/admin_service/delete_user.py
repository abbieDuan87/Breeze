from breeze.services.admin_service.admin_user_printer import print_users
from breeze.utils.cli_utils import check_exit, clear_screen, direct_to_dashboard, print_system_message
from breeze.utils.constants import ADMIN_BANNER_STRING

def delete_user(auth_service):
    clear_screen()
    print(ADMIN_BANNER_STRING)
    print_system_message("Delete a User")

    users_to_delete = [user for user in auth_service.users.values() if user.get_role() in ["Patient", "MHWP"]]
    print_users(users_to_delete, "All Users", basic_view=True)
    print("\nEnter the username of the user to delete (or press [X] to exit):")
    while True:
        
        username = input("> ").strip().lower()

        if check_exit(username):
            break

        user_to_delete = auth_service.users.get(username)
        if not user_to_delete or user_to_delete.get_role() == "Admin" or user_to_delete.get_role() not in ["Patient", "MHWP"]:
            print_system_message("Invalid username. Please try again.")
            continue

        clear_screen()
        print(ADMIN_BANNER_STRING)
        print_users(users_to_delete, "Remaining Users", basic_view=True)


        print_system_message(f"Are you sure you want to delete the user '{username}'? Type [Y] to confirm or [N] to cancel:")
        while True:
            confirmation = input("> ").strip().lower()
            if confirmation == "y":
                del auth_service.users[username]
                auth_service.save_data_to_file()

                users_to_delete = [user for user in users_to_delete if user.get_username() != username]
                clear_screen()
                print(ADMIN_BANNER_STRING)
                print_users(users_to_delete, "Remaining Users", basic_view=True)

                print_system_message(f"User '{username}' has been successfully deleted.")
                direct_to_dashboard()
                return
            elif confirmation == "n":
                print_system_message("Deletion cancelled. You can select another user to delete or press [X] to exit.")
                break
            else:
                print_system_message("Invalid input. Please type [Y] to confirm or [N] to cancel.")