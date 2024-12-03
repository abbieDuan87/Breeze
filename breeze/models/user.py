class User:
    """The basic User class
    """
    def __init__(self, username, password, role, email=None, first_name=None, last_name=None, date_of_birth=None, gender=None, is_disabled=False):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__is_disabled = is_disabled
        
    def get_username(self):
        return self.__username
        
    def get_password(self):
        return self.__password
    
    def get_role(self):
        return self.__role
    
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def get_email(self):
        return self.__email
    
    def get_full_name(self):
        if not self.__first_name or not self.__last_name:
            return None
        return f'{self.__first_name} {self.__last_name}'
    
    def get_is_disabled(self):
        return self.__is_disabled

    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password
    
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email
          
    def set_is_disabled(self, is_disabled):
        self.__is_disabled = is_disabled

    def login(self, input_password):
        return self.get_password() == input_password