from breeze.services.patient_service.appointment import manage_appointment
from breeze.services.patient_service.exercise import search_exercise
from breeze.services.patient_service.journal import enter_journal
from breeze.services.patient_service.mood import record_mood
from breeze.services.patient_service.personal_info import edit_personal_information
from breeze.services.patient_service.history import show_history
from .patient_dashboard import show_patient_dashboard


class PatientService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def show_patient_dashboard(self, user):
        return show_patient_dashboard(user, self)

    def edit_personal_information(self, user):
        edit_personal_information(user, self.auth_service)

    def record_mood(self, user):
        record_mood(user, self.auth_service)

    def enter_journaling(self, user):
        enter_journal(user, self.auth_service)
    
    def search_exercise(self, user):
        search_exercise()

    def manage_appointment(self, user):
        manage_appointment(user, self.auth_service)

    def show_history(self, user):
        show_history(user)