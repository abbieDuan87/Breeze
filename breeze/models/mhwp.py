from .user import User
from ..utils.calendar_utils import (
    get_next_available_days,
    generate_time_slots,
    generate_calendar_slot_code_map,
)

import datetime

from .appointment_entry import AppointmentEntry


class MHWP(User):
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
        self.__assigned_patients = assigned_patients if assigned_patients is not None else []

    def get_appointments(self):
        return self.__appointments

    def set_appointments(self, appointments):
        self.__appointments = appointments

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def get_appointment_by_date_time(self, date, time):
        """Searches for an appointment by date and time.

        Args:
            date (str/datetime): "%Y-%m-%d"
            time (str): "%I:%M %p"

        Returns:
            AppointmentEntry/None: the founded AppointmentEntry or None
        """
        date_obj = (
            datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if isinstance(date, str)
            else date
        )
        time_obj = datetime.datetime.strptime(time, "%I:%M %p").time()

        for app in self.get_appointments():
            if app.get_date() == date_obj and app.get_time() == time_obj:
                return app
        return None

    def display_calendar(self, code_map=None):
        """
        Displays the calendar with dates as columns and time slots as rows for this MHWP.
        """
        next_available_days = get_next_available_days()
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

        print(
            f"\nUpcoming Calendar for {self.get_username()} in the next five working days ({date_range}):"
        )
        print("+", "-" * (10 + 17 * len(next_available_days)), "+")

        print(f"| {'Time':<10}", end=" | ")
        for day in next_available_days:
            print(f"{day.strftime('%Y-%m-%d %a'):<14}", end=" | ")
        print()
        print("+", "-" * (10 + 17 * len(next_available_days)), "+")

        for i, slot in enumerate(time_slots):
            print(f"| {slot:<10}", end=" | ")
            for j, day in enumerate(next_available_days):
                code = f"{chr(ord('A') + i)}{j + 1}"
                day_slot = code_map[code]

                app = self.get_appointment_by_date_time(day_slot[0], day_slot[1])
                placeholder = app.get_status() if app else code
                print(f"{placeholder:<14}", end=" | ")
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
            "assignedPatients": self.__assigned_patients
        }


if __name__ == "__main__":
    gp1 = MHWP(username="gp1", password="")
    app1 = AppointmentEntry("2024-11-21", "10:00 AM")
    gp1.add_appointment(app1)
    app1.request_appointment()
    print(gp1.get_appointments()[0])
    print(gp1.get_appointment_by_date_time("2024-11-21", "10:00 AM"))
    gp1.display_calendar()
