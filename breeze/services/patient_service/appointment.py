import time
from breeze.models.appointment_entry import AppointmentEntry
from breeze.utils.calendar_utils import generate_calendar_slot_code_map
from breeze.utils.cli_utils import (
    clear_screen,
    direct_to_dashboard,
    print_appointments,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def manage_appointment(user, auth_service):
    """
    Allows the patient to book and manage upcoming appointments.
    """

    def show_upcoming_appointments():
        """Displays the patient's upcoming appointments."""
        upcoming_appointments = sorted(
            user.get_appointments(), key=lambda app: (app.get_date(), app.get_time())
        )
        if upcoming_appointments:
            print("\nHere are your upcoming appointments:")
            print_appointments(upcoming_appointments)
            return upcoming_appointments

        else:
            print("You have no upcoming appointment.")

    def display_mhwp_selection():
        """Displays available MHWPs for the patient to choose from."""
        available_mhwps = [
            user
            for user in auth_service.get_all_users().values()
            if user.get_role().lower() == "mhwp"
        ]
        if not available_mhwps:
            print("No MHWPs are currently available.")
            return None
        print_mhwps_for_selection(available_mhwps, user)
        return available_mhwps

    def print_mhwps_for_selection(mhwps, user):
        """
        Prints an ASCII table of MHWP options for a user to choose from, displaying only the MHWP's username and
        a flag if it is the user's assigned GP.

        :param mhwps: List of MHWP objects.
        :param user: The user object, to check if the MHWP is the assigned GP.
        """
        if not mhwps:
            print("No MHWPs available for selection.")
            return

        headers = ["Username", "Assigned GP"]

        rows = [
            [
                mhwp.get_username(),
                "Yes" if mhwp.get_username() == user.get_assigned_mhwp() else "No",
            ]
            for mhwp in mhwps
        ]

        column_widths = [
            max(len(row[i]) for row in rows + [headers]) for i in range(len(headers))
        ]

        separator = "+".join("-" * (width + 2) for width in column_widths)
        separator = f"+{separator}+"

        print(separator)
        print(
            "| "
            + " | ".join(
                header.center(width) for header, width in zip(headers, column_widths)
            )
            + " |"
        )
        print(separator)
        for row in rows:
            print(
                "| "
                + " | ".join(
                    cell.ljust(width) for cell, width in zip(row, column_widths)
                )
                + " |"
            )
        print(separator)

    def clear_screen_and_show_header():
        clear_screen()
        print(PATIENT_BANNER_STRING)

    def confirm_user_choice(
        on_confirm=lambda: print("Action confirmed."),
        on_cancel=lambda: print("Action canceled."),
    ):
        while True:
            print("\nPress [Y] for confirm and [N] for cancel:")
            user_choice = input("> ").strip().lower()
            if user_choice == "y":
                on_confirm()
                break
            elif user_choice == "n":
                on_cancel()
                break

    def handle_confirm_appointment(user, selected_mhwp, requested_app):
        user.add_appointment(requested_app)
        selected_mhwp.add_appointment(requested_app)
        print("Appointment confirmed and added.")

    while True:
        clear_screen_and_show_header()

        assigned_mhwp = user.get_assigned_mhwp()
        if assigned_mhwp:
            print(f"Your current assigned MHWP: {assigned_mhwp}.")
        else:
            print("Your have no assigned MHWP.")

        show_upcoming_appointments()

        print("\nChoose one of the following options:")
        print("\n[B]ook an appointment\n[C]ancel an upcoming appointment\n[E]xit\n")
        user_choice = input("> ").strip().lower()

        if user_choice == "b":
            while True:
                clear_screen_and_show_header()
                print("\nChoose the MHWP from the following list:")
                available_mhwps = display_mhwp_selection()

                if not available_mhwps:
                    print_system_message("No available MHWPs to book an appointment.")
                    continue

                print("\nEnter the MHWP's username (or press [r] to cancel):")
                selected_mhwp_username = input("> ").strip().lower()
                if selected_mhwp_username == "r":
                    break

                selected_mhwp = next(
                    (
                        mhwp
                        for mhwp in available_mhwps
                        if mhwp.get_username() == selected_mhwp_username
                    ),
                    None,
                )

                if selected_mhwp:
                    clear_screen_and_show_header()
                    app_code_map = generate_calendar_slot_code_map()

                    while True:
                        clear_screen_and_show_header()
                        selected_mhwp.display_calendar()
                        print(
                            "\nSelect the available slot from the calendar (press [r] to cancel):"
                        )
                        selected_slot = (
                            input("> ").strip().upper()
                        )  # the codes are all upper case

                        if selected_slot.lower() == "r":  # but the return is lower case
                            break
                        elif selected_slot in app_code_map:
                            app_date_time_tuple = app_code_map.get(selected_slot)
                            requested_app = AppointmentEntry(
                                app_date_time_tuple[0],
                                app_date_time_tuple[1],
                                mhwp_username=selected_mhwp_username,
                                patient_username=user.get_username(),
                            )
                            requested_app.request_appointment()

                            print("\nPlease check the details for the appointment:")
                            print_appointments([requested_app])

                            confirm_user_choice(
                                on_confirm=lambda: handle_confirm_appointment(
                                    user, selected_mhwp, requested_app
                                ),
                                on_cancel=lambda: print(
                                    "Appointment request canceled."
                                ),
                            )
                            auth_service.save_data_to_file()
                            print_system_message(
                                "Appointment request sent successfully!"
                            )
                            time.sleep(1)
                            break

                        else:
                            print_system_message("Invalid slot, please try again!")
                            time.sleep(0.5)
                else:
                    print_system_message("Cannot find this MHWP, please try again!")
                    time.sleep(0.5)

        elif user_choice == "c":
            while True:
                clear_screen_and_show_header()

                upcoming_appointments = show_upcoming_appointments()

                if not upcoming_appointments:
                    break

                print(
                    "\nEnter the index number of the appointment you want to cancel (or type 'r' to return):"
                )
                selected_appointment_index = input("> ").strip().lower()

                if selected_appointment_index == "r":
                    break

                try:
                    selected_index = int(selected_appointment_index)
                    if selected_index < 1 or selected_index > len(
                        upcoming_appointments
                    ):
                        print_system_message(
                            "Invalid appointment index number. Please try again."
                        )
                        time.sleep(0.5)
                        continue

                    appointment_to_cancel = upcoming_appointments[selected_index - 1]
                    if appointment_to_cancel:
                        print_system_message(
                            f"Appointment {selected_index} will be canceled."
                        )
                        appointment_to_cancel.cancel_appointment()
                        auth_service.save_data_to_file()
                        time.sleep(1)

                        print_system_message(
                            f"Appointment {selected_index} has been canceled."
                        )
                        time.sleep(1)

                except ValueError:
                    print_system_message("Please enter a valid number.")
                    time.sleep(0.5)
                    continue

        elif user_choice == "e":
            direct_to_dashboard()
            break
        else:
            print_system_message("Please enter a valid option.")
            time.sleep(0.5)
