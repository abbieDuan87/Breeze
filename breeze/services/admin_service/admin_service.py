
from breeze.services.admin_service.admin_dashboard import show_admin_dashboard
from breeze.services.admin_service.delete_user import delete_user
from breeze.services.admin_service.disable_user import disable_user
from breeze.services.admin_service.edit_user_infomation import edit_user_information
from breeze.services.admin_service.patient_mhwp_allocation import reallocate_patient_to_mhwp
from breeze.services.admin_service.view_summary import view_summary


class AdminService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def show_admin_dashboard(self, user):
        return show_admin_dashboard(user, self)

    def reallocate_patient_to_mhwp(self):
        reallocate_patient_to_mhwp(self.auth_service)

    def edit_user_information(self):
        edit_user_information(self.auth_service)

    def delete_user(self):
        delete_user(self.auth_service)

    def disable_user(self):
        disable_user(self.auth_service)

    def view_summary(self):
        view_summary(self.auth_service)