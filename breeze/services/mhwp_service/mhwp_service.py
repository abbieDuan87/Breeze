from breeze.services.mhwp_service.add_patient_information import add_patient_information
from breeze.services.mhwp_service.display_patient_summary import display_patient_summary
from breeze.services.mhwp_service.edit_personal_information import edit_personal_information
from breeze.services.mhwp_service.manage_appointments import manage_appointments
from breeze.services.mhwp_service.show_mhwp_dashboard import show_mhwp_dashboard
from breeze.services.mhwp_service.view_calendar import view_calendar


class MHWPService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def show_mhwp_dashboard(self, user):
        return show_mhwp_dashboard(user, self)
    
    def view_calendar(self, user):
        view_calendar(user)

    def manage_appointments(self, user):
        manage_appointments(user, self.auth_service)

    def add_patient_information(self, user):
        add_patient_information(user, self.auth_service)
    
    def display_patient_summary(self, user):
        display_patient_summary(user, self.auth_service)
    
    def edit_personal_information(self, user):
        edit_personal_information(user, self.auth_service)
