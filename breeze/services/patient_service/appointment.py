import time
from breeze.models.appointment_entry import AppointmentEntry
from breeze.services.email_service import EmailService
from breeze.utils.appointment_utils import (
    confirm_user_choice,
    handle_appointment_action,
    show_upcoming_appointments,
)
from breeze.utils.calendar_utils import generate_calendar_slot_code_map
from breeze.utils.cli_utils import (
    check_exit,
    clear_screen_and_show_banner,
    print_appointments,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def manage_appointment(user, auth_service):
    """
    Allows the patient to book and manage upcoming appointments.
    """

    def handle_confirm_appointment(user, selected_mhwp, requested_app):
        user.add_appointment(requested_app)
        selected_mhwp.add_appointment(requested_app)
        print("Appointment confirmed and added.")

    while True:
        clear_screen_and_show_banner(PATIENT_BANNER_STRING)
        print(f"Hi, {user.get_username()} !")

        assigned_mhwp = user.get_assigned_mhwp()
        if assigned_mhwp:
            print(f"Your current assigned MHWP: {assigned_mhwp}.")
        else:
            print("You have no assigned MHWP.")

        show_upcoming_appointments(user)

        print("\nChoose one of the following options:")
        print(
            "\n[B] Book an appointment\n[C] Cancel an upcoming appointment\n[X] Exit\n"
        )
        user_choice = input("> ").strip().lower()
        if check_exit(user_choice):
            return

        if user_choice == "b":
            while True:
                clear_screen_and_show_banner(PATIENT_BANNER_STRING)
                print(f"Hi, {user.get_username()} !")

                assigned_mhwp_username = user.get_assigned_mhwp()
                assigned_mhwp_object = auth_service.get_user_by_username(
                    assigned_mhwp_username
                )
                if not assigned_mhwp_object:
                    print(
                        "You have no assigned MHWP at this moment, contact the admin for more info."
                    )
                    time.sleep(1)
                    break

                if assigned_mhwp_object:
                    clear_screen_and_show_banner(PATIENT_BANNER_STRING)
                    app_code_map = generate_calendar_slot_code_map()

                    assigned_mhwp_object.display_calendar(is_MHWP_view=False)
                    print(
                        "\nSelect the available slot from the calendar (or enter [X] to exit):"
                    )
                    selected_slot = (
                        input("> ").strip().upper()
                    )  # the codes are all upper case

                    if check_exit(selected_slot):
                        break
                    elif selected_slot in app_code_map:
                        app_date_time_tuple = app_code_map.get(selected_slot)

                        checked_mhwp_app = (
                            assigned_mhwp_object.get_appointment_by_date_time(
                                app_date_time_tuple[0], app_date_time_tuple[1]
                            )
                        )
                        checked_patient_app = user.get_appointment_by_date_time(
                            app_date_time_tuple[0], app_date_time_tuple[1]
                        )
                        if (
                            checked_mhwp_app
                            and checked_mhwp_app.get_status() != "cancelled"
                        ):
                            print_system_message(
                                "This slot has already been requested or confirmed. Please select a different one"
                            )
                            time.sleep(1)
                            continue

                        if (
                            checked_patient_app
                            and checked_patient_app.get_status() != "cancelled"
                        ):
                            print_system_message(
                                "You have another appointment at the same time. Please select a different one"
                            )
                            time.sleep(1)
                            continue

                        requested_app = AppointmentEntry(
                            app_date_time_tuple[0],
                            app_date_time_tuple[1],
                            mhwp_username=assigned_mhwp_object.get_username(),
                            patient_username=user.get_username(),
                        )
                        requested_app.request_appointment()

                        print("\nPlease check the details for the appointment:")
                        print_appointments([requested_app])

                        is_confirmed_choice = confirm_user_choice(
                            on_confirm=lambda: handle_confirm_appointment(
                                user, assigned_mhwp_object, requested_app
                            ),
                            on_cancel=lambda: print("Appointment request cancelled."),
                        )

                        if not is_confirmed_choice:
                            time.sleep(1)
                            continue

                        auth_service.save_data_to_file()
                        print_system_message("Appointment request sent successfully!")

                        email_service = EmailService(requested_app, auth_service)
                        email_service.send_to_one("mhwp", "request")
                        time.sleep(3)

                        break

                    else:
                        print_system_message("Invalid slot, please try again!")
                        time.sleep(1)

        elif user_choice == "c":
            while True:
                clear_screen_and_show_banner(PATIENT_BANNER_STRING)
                print(f"Hi, {user.get_username()} !")

                upcoming_appointments = show_upcoming_appointments(user)

                if not upcoming_appointments:
                    time.sleep(1)
                    break

                print(
                    "\nEnter the index number of the appointment you want to cancel (or enter [X] to exit):"
                )
                selected_appointment_index = input("> ").strip().lower()

                if check_exit(selected_appointment_index):
                    break

                try:
                    selected_index = int(selected_appointment_index)

                    if not handle_appointment_action(
                        upcoming_appointments, selected_index, auth_service
                    ):
                        print_system_message("Action could not be completed.")

                except ValueError as ve:
                    if "invalid literal for int()" in str(ve):
                        print_system_message("Please enter a valid number.")
                    else:
                        print_system_message(str(ve))

                    time.sleep(1)
                    continue
        else:
            print_system_message("Please enter a valid option.")
            time.sleep(1)
