from .user import User

class MHWP(User):
    def __init__(self, username, password, first_name = None, last_name = None, email= None, is_disabled=False, appointments=[], assigned_patients=[]):
        super().__init__(username, password, role='MHWP', first_name= first_name, last_name= last_name, email= email, is_disabled=is_disabled)
        self.__appointments = appointments
        self.__assigned_patients = assigned_patients

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
                "email": self.get_email()},
            "appointments": self.__appointments,
            "assignedPatients": self.__assigned_patients
        }
        