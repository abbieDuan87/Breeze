from breeze.models.appointment_mixin import AppointmentMixin
from .user import User


class Patient(User, AppointmentMixin):
    def __init__(
        self,
        username,
        password,
        first_name=None,
        last_name=None,
        email=None,
        emergency_contact_email=None,
        date_of_birth=None,
        gender=None,
        is_disabled=False,
        mood_entries=[],
        journal_entries=[],
        appointments=[],
        assigned_MHWP=None,
    ):
        super().__init__(
            username,
            password,
            role="Patient",
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_disabled=is_disabled,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        self.__emergency_contact_email = emergency_contact_email
        self.__mood_entries = mood_entries
        self.__journal_entries = journal_entries
        self.__appointments = appointments
        self.__assigned_mhwp = assigned_MHWP
        self.__conditions = {}
        self.__prescriptions = []
    
    def get_emergency_contact(self):
        return self.__emergency_contact_email

    def set_emergency_contact(self, email):
        self.__emergency_contact_email = email

    def get_mood_entries(self):
        return self.__mood_entries

    def get_appointments(self):
        return self.__appointments

    def set_appointments(self, appointments):
        self.__appointments = appointments

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def add_mood_entry(self, mood_id, mood, comment, datetime_str):
        self.__mood_entries.append(
            {"id": mood_id, "mood": mood, "comment": comment, "datetime": datetime_str}
        )

    def add_journal_entry(self, journal_id, title, entry, datetime_str):
        self.__journal_entries.append(
            {"id": journal_id, "title": title, "entry": entry, "datetime" : datetime_str}
        )

    def get_assigned_mhwp(self):
        return self.__assigned_mhwp

    def set_assigned_mhwp(self, mhwp_username):
        self.__assigned_mhwp = mhwp_username
    
    def add_condition(self, condition, notes):
        self.__conditions[condition] = notes

    def add_prescription(self, medication, dosage, frequency, start_date, end_date, notes):
        self.__prescriptions.append({
            "medication": medication,
            "dosage": dosage,
            "frequency": frequency,
            "start_date": start_date,
            "end_date": end_date,
            "notes": notes
        })    

    def __str__(self):
        return f"Patient: {self.get_username()}, Role: {self.get_role()}"

    def __repr__(self):
        return f"Patient(username={self.get_username()}, role={self.get_role()})"

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
                "emergencyContactEmail": self.get_emergency_contact(),
                "gender": self.get_gender(),
                "dateOfBirth": self.get_date_of_birth(),
            },
            "assignedMHWP": self.get_assigned_mhwp(),
            "moods": self.__mood_entries,
            "journals": self.__journal_entries,
            "appointments": [app.get_id() for app in self.get_appointments()],
            "conditions": self.__conditions,  
            "prescriptions": self.__prescriptions
        }