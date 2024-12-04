import datetime


class AppointmentMixin:
    def get_appointment_by_date_time(self, date, time, not_cancelled=True):
        """Searches for an appointment by date and time."""
        date_obj = (
            datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if isinstance(date, str)
            else date
        )
        time_obj = datetime.datetime.strptime(time, "%I:%M %p").time()

        for app in self.get_appointments():
            if app.get_date() == date_obj and app.get_time() == time_obj:
                if not_cancelled and app.get_status() != "cancelled":
                    return app
                elif not_cancelled is False:
                    return app
        return None
