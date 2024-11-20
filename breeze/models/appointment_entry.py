import uuid
from datetime import datetime, time, date


class AppointmentEntry:
    def __init__(
        self,
        date_str,
        time_str,
        isCancelled=False,
        status=None,
        mhwp_username=None,
        patient_username=None,
        appointment_id=None,
    ):
        """
        Initialises an appointment entry.

        Args:
            date_str (str): Date of the appointment in 'YYYY-MM-DD' format.
            time_str (str): Time of the appointment in 'HH:MM AM/PM' format.
            isCancelled (bool): Whether the appointment is cancelled.
            status (str): The status of the appointment (e.g., "requested", "confirmed", "cancelled").
        """
        self.appointment_id = appointment_id or str(uuid.uuid4())
        # Handle date input
        if isinstance(date_str, date):
            self.date = date_str
        else:
            self.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Handle time input
        if isinstance(time_str, time):
            self.time = time_str
        else:
            self.time = datetime.strptime(time_str, "%I:%M %p").time()
        self.mhwp_username = mhwp_username
        self.patient_username = patient_username
        self.isCancelled = isCancelled
        self.status = status  # "requested", "confirmed", or "cancelled"

    def get_id(self):
        return self.appointment_id

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_status(self):
        return self.status

    def is_cancelled(self):
        return self.isCancelled

    def cancel_appointment(self):
        """
        Marks the appointment as cancelled and updates status.
        """
        self.isCancelled = True
        self.status = "cancelled"

    def confirm_appointment(self):
        """
        Marks the appointment as confirmed and updates status.
        """
        self.status = "confirmed"

    def request_appointment(self):
        """
        Marks the appointment as requested and updates status.
        """
        self.status = "requested"

    def __str__(self):
        return (
            f"AppointmentEntry(\n"
            f"  id={self.appointment_id},\n"
            f"  date={self.date},\n"
            f"  time={self.time},\n"
            f"  status={self.status},\n"
            f"  cancelled={self.isCancelled},\n"
            f"  patient={self.patient_username},\n"
            f"  mhwp={self.mhwp_username}\n"
            f")"
        )

    def to_dict(self):
        """
        Converts the AppointmentEntry object into a dictionary representation.

        Returns:
            dict: Dictionary representation of the appointment entry.
        """
        return {
            "appointmentId": self.appointment_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "time": self.time.strftime("%I:%M %p"),
            "isCancel": self.isCancelled,
            "status": self.status,
            "mhwpUsername": self.mhwp_username,
            "patientUsername": self.patient_username,
        }
