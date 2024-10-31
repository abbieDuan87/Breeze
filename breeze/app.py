from breeze.services.auth_service import AuthService
from breeze.services.admin_service import AdminService
from breeze.services.patient_service import PatientService
from breeze.services.mhwp_service import MHWPService

class BreezeApp:
    def __init__(self):
        self.auth_service = AuthService()
        self.admin_service = AdminService()
        self.patient_service = PatientService()
        self.mhwp_service = MHWPService()
    
    def run(self):
        print("Welcome to Breeze - Mental Health Management System")
        self.show_login()

    def show_login(self):
        user = self.auth_service.login()
        if user:
            self.show_dashboard(user)
        else:
            print("Invalid credentials, try again.")
            self.show_login()

    def show_dashboard(self, user):
        if user.role == "Admin":
            self.admin_service.show_admin_dashboard(user)
        elif user.role == "Patient":
            self.patient_service.show_patient_dashboard(user)
        elif user.role == "MHWP":
            self.mhwp_service.show_mhwp_dashboard(user)
        else:
            print("Unknown user type.")