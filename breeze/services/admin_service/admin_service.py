from breeze.services.admin_service.admin_dashboard import show_admin_dashboard
from breeze.services.admin_service.user_management import (
    edit_user_information,
    delete_user,
    disable_user,
)
from breeze.services.admin_service.patient_mhwp_allocation import allocate_patient_to_mhwp
from breeze.services.admin_service.view_summary import view_summary
from breeze.utils.print_patinet_utils import _print_users, _print_users_with_disabled_status


class AdminService:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def show_admin_dashboard(self, user):
        return show_admin_dashboard(user, self)

    def allocate_patient_to_mhwp(self):
        allocate_patient_to_mhwp(self.auth_service)

    def edit_user_information(self):
        edit_user_information(self.auth_service)

    def delete_user(self):
        delete_user(self.auth_service)

    def disable_user(self):
        disable_user(self.auth_service)

    def view_summary(self):
        view_summary(self.auth_service)
    
    def _print_users(self, users, title, show_assigned_patients=False):
        _print_users(users, title, show_assigned_patients)

    def _print_users_with_disabled_status(self):
        _print_users_with_disabled_status(self.auth_service)