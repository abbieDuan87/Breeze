from .user import User

class MHWP(User):
    def __init__(self, username, password, is_disabled=False, appointments=[]):
        super().__init__(username, password, role='MHWP', is_disabled=is_disabled)
        self.__appointments = appointments
    
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
            "appointments": self.__appointments
        }
        