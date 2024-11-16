from .user import User

class MHWP(User):
    def __init__(self, username, password, first_name = None, last_name = None, email= None, is_disabled=False, appointments=[]):
        super().__init__(username, password, role='MHWP', is_disabled=is_disabled)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__appointments = appointments
    
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email

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
            "appointments": self.__appointments
        }
        