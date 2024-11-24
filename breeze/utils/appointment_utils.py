import time
import datetime
from breeze.utils.cli_utils import print_appointments, print_system_message
from breeze.services.email_service import EmailService


def confirm_user_choice(
    on_confirm=lambda: print("Action confirmed."),
    on_cancel=lambda: print("Action cancelled."),
):
    while True:
        print("\nPress [Y] for confirm and [N] for cancel:")
        user_choice = input("> ").strip().lower()
        if user_choice == "y":
            on_confirm()
            return True
        elif user_choice == "n":
            on_cancel()
            return False


def show_upcoming_appointments(
    user, key=(lambda app: (app.get_date(), app.get_time()))
):
    """Displays the user's upcoming appointments."""
    upcoming_appointments = sorted(
        [
            app
            for app in user.get_appointments()
            if app.get_date() > datetime.datetime.now().date()
        ],
        key=key,
    )
    if upcoming_appointments:
        print("\nHere are your upcoming appointments:")
        print_appointments(upcoming_appointments)
        return upcoming_appointments
    else:
        print("You have no upcoming appointment.")
        return []


def handle_appointment_action(
    upcoming_appointments, selected_index, auth_service, action="cancel"
):
    if action not in {"cancel", "confirm"}:
        raise ValueError(f"Invalid action '{action}'. Must be 'cancel' or 'confirm'.")

    if not (1 <= selected_index <= len(upcoming_appointments)):
        print_system_message("Invalid appointment index. Please try again.")
        time.sleep(1)
        return False

    appointment = upcoming_appointments[selected_index - 1]
    if not appointment:
        print_system_message("No appointment found at the given index.")
        time.sleep(1)
        return False

    if action == "cancel" and appointment.get_status() == "cancelled":
        print_system_message("This appointment is already cancelled. No action needed.")
        time.sleep(1)
        return False
    elif action == "confirm" and appointment.get_status() == "confirmed":
        print_system_message("This appointment is already confirmed. No action needed.")
        time.sleep(1)
        return False

    if action == "cancel":
        appointment.cancel_appointment()
    elif action == "confirm":
        appointment.confirm_appointment()

    auth_service.save_data_to_file()

    print_system_message(
        f"Appointment {selected_index} has been successfully {action}ed."
    )

    email_service = EmailService(appointment, auth_service)
    email_service.send_to_both(action)
    time.sleep(2.5)

    return True
