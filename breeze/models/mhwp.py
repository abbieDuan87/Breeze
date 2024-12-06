from breeze.models.appointment_mixin import AppointmentMixin
from breeze.utils.ansi_utils import colorise
from .user import User
from ..utils.calendar_utils import (
    get_colored_status,
    get_next_available_days,
    generate_time_slots,
    generate_calendar_slot_code_map,
    strip_ansi_codes,
)

import datetime

from .appointment_entry import AppointmentEntry


class MHWP(User, AppointmentMixin):
    def __init__(
        self,
        username,
        password,
        first_name=None,
        last_name=None,
        email=None,
        is_disabled=False,
        appointments=None,
        assigned_patients=None,
    ):
        super().__init__(
            username,
            password,
            role="MHWP",
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_disabled=is_disabled,
        )
        self.__appointments = appointments if appointments is not None else []
        self.__assigned_patients = (
            assigned_patients if assigned_patients is not None else []
        )

    def get_appointments(self):
        return self.__appointments

    def set_appointments(self, appointments):
        self.__appointments = appointments

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def display_calendar(self, code_map=None, is_MHWP_view=True):
        """
        Displays the calendar with dates as columns and time slots as rows for this MHWP.
        """
        HEADER_WIDTH = 116

        next_available_days = get_next_available_days(include_today=True)
        time_slots = generate_time_slots()
        code_map = (
            generate_calendar_slot_code_map(next_available_days, time_slots)
            if not code_map
            else code_map
        )

        if next_available_days:
            start_date = next_available_days[0].strftime("%m-%d")
            end_date = next_available_days[-1].strftime("%m-%d")
            date_range = f"{start_date} ~ {end_date}"
        else:
            date_range = "No available days"

        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y %a")

        header_line = "=" * HEADER_WIDTH
        sub_header_line = "-" * HEADER_WIDTH

        print(f"\n{header_line}")
        print(f"Today is {formatted_date}".center(HEADER_WIDTH))

        text_with_colors = (
            f"Upcoming calendar for {colorise(self.get_username(), color=63)} {colorise('today', bold=True)}, and for the "
            f"{colorise(f'next five working days ({date_range})', bold=True)}:"
        )
        text_without_colors = strip_ansi_codes(text_with_colors)

        print(
            text_with_colors.center(
                HEADER_WIDTH + (len(text_with_colors) - len(text_without_colors))
            )
        )

        upcoming_appointments = [
            app
            for app in self.get_appointments()
            if app.get_status() != "cancelled" and app.get_date() >= current_date.date()
        ]
        requested_appointments_count = len(
            [app for app in upcoming_appointments if app.get_status() == "requested"]
        )
        confirmed_appointments_count = len(
            [app for app in upcoming_appointments if app.get_status() == "confirmed"]
        )

        print(
            f"Number of requested appointments: {requested_appointments_count}".center(
                HEADER_WIDTH
            )
        )
        print(
            f"Number of confirmed appointments: {confirmed_appointments_count}".center(
                HEADER_WIDTH
            )
        )

        print(f"{sub_header_line}\n")

        print("+", "-" * (10 + 17 * len(next_available_days)), "+")
        print(f"| {'Time':<10}", end=" | ")
        for day in next_available_days:
            if day == datetime.date.today():
                print(f"{'Today':<14}", end=" | ")
            else:
                print(f"{day.strftime('%d-%m-%Y %a'):<14}", end=" | ")
        print()
        print("+", "-" * (10 + 17 * len(next_available_days)), "+")

        for i, slot in enumerate(time_slots):
            print(f"| {slot:<10}", end=" | ")
            for j, day in enumerate(next_available_days):
                code = f"{chr(ord('A') + i)}{j + 1}"
                day_slot = code_map[code]

                app = self.get_appointment_by_date_time(day_slot[0], day_slot[1])
                if is_MHWP_view:
                    placeholder = (
                        get_colored_status(app.get_status())
                        if app and app.get_status() != "cancelled"
                        else "\u25CB"
                    )
                else:
                    if app and app.get_status() == "confirmed":
                        placeholder = get_colored_status("unavailable")
                    else:
                        if app and app.get_status() != "cancelled":
                            placeholder = get_colored_status(app.get_status())
                        else:
                            placeholder = code

                    if day == datetime.date.today():
                        day_slot_time_obj = datetime.datetime.strptime(
                            day_slot[1], "%I:%M %p"
                        )
                        now = datetime.datetime.now()

                        day_slot_time_obj = now.replace(
                            hour=day_slot_time_obj.hour,
                            minute=day_slot_time_obj.minute,
                            second=0,
                            microsecond=0,
                        )

                        two_hours_ahead = day_slot_time_obj - datetime.timedelta(
                            hours=2
                        )

                        if now >= two_hours_ahead:
                            placeholder = "\u25CB"

                visible_placeholder = strip_ansi_codes(placeholder)
                padding_width = 14 - len(visible_placeholder) + len(placeholder)

                print(f"{placeholder:<{padding_width}}", end=" | ")
            print()

        print("+", "-" * (10 + 17 * len(next_available_days)), "+")

    def add_patient(self, patient_username):
        if patient_username not in self.__assigned_patients:
            self.__assigned_patients.append(patient_username)

    def get_assigned_patients(self):
        return self.__assigned_patients

    def __str__(self):
        return f"MHWP: {self.get_username()}, Role: {self.get_role()}"

    def __repr__(self):
        return f"MHWP(username={self.get_username()}, role={self.get_role()})"

    def to_dict(self):
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "role": self.get_role(),
            "isDisabled": self.get_is_disabled(),
            "information": {
                "firstName": self.get_first_name(),
                "lastName": self.get_last_name(),
                "email": self.get_email(),
            },
            "appointments": [app.get_id() for app in self.get_appointments()],
            "assignedPatients": self.__assigned_patients,
        }


if __name__ == "__main__":
    gp1 = MHWP(username="gp1", password="")
    app1 = AppointmentEntry("2024-11-25", "10:00 AM")
    app2 = AppointmentEntry("2024-11-25", "11:00 AM")
    gp1.add_appointment(app1)
    gp1.add_appointment(app2)
    app1.request_appointment()
    app2.confirm_appointment()
    # print(gp1.get_appointments())
    # print("app1:", gp1.get_appointment_by_date_time("2024-11-22", "10:00 AM"))
    # print("app2:", gp1.get_appointment_by_date_time("2024-11-23", "11:00 AM"))

    gp1.display_calendar(is_MHWP_view=True)
