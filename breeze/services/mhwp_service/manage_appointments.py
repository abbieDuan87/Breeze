import time
from breeze.utils.appointment_utils import (
    cancel_appointments_with_inactive_accounts,
    handle_appointment_action,
    show_upcoming_appointments,
)
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen_and_show_banner,
    print_system_message,
)
from breeze.utils.constants import MHWP_BANNER_STRING


def manage_appointments(user, auth_service):
    def handle_action(upcoming_appointments, action, prompt):
        """Reusable logic to handle appointment actions (cancel or confirm)."""
        while True:
            clear_screen_and_show_banner(MHWP_BANNER_STRING)
            cancel_appointments_with_inactive_accounts(
                auth_service, user.get_appointments()
            )
            upcoming_appointments = show_upcoming_appointments(
                user,
                auth_service,
                (
                    lambda app: (
                        app.get_date(),
                        app.get_time(),
                        app.patient_username,
                    )
                ),
            )

            print(
                f"\nEnter the index number of the appointment you want to {action} (or enter [R] to return to previous menu):"
            )
            selected_index_input = input("> ").strip().lower()

            if selected_index_input == "r":
                break

            try:
                selected_index = int(selected_index_input)

                if not handle_appointment_action(
                    upcoming_appointments, selected_index, auth_service, action
                ):
                    print_system_message("Action could not be completed.")

            except ValueError as ve:
                if "invalid literal for int()" in str(ve):
                    print_system_message("Please enter a valid number.")
                else:
                    print_system_message(str(ve))

                time.sleep(1)
                continue

    while True:
        clear_screen_and_show_banner(MHWP_BANNER_STRING)
        print(f"Hi, {user.get_username()} !")
        cancel_appointments_with_inactive_accounts(
            auth_service, user.get_appointments()
        )
        upcoming_appointments = show_upcoming_appointments(
            user,
            auth_service,
            (lambda app: (app.get_date(), app.get_time(), app.patient_username)),
        )

        if not upcoming_appointments:
            time.sleep(1)
            break

        print("\nChoose one of the following options:")
        print("\n[C] Cancel appointments\n[F] Confirm appointments\n[X] Exit\n")

        selected_action = input("> ").strip().lower()

        if check_exit(selected_action):
            break

        if selected_action == "c":
            handle_action(upcoming_appointments, "cancel", "Cancel")
        elif selected_action == "f":
            handle_action(upcoming_appointments, "confirm", "Confirm")
        else:
            print_system_message("Please enter a valid option.")
            time.sleep(0.5)
