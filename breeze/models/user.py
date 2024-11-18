class User:
    """The basic User class
    """
    def __init__(self, username, password, role, is_disabled=False):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__is_disabled = is_disabled
        
    def get_username(self):
        return self.__username
        
    def get_password(self):
        return self.__password
    
    def get_role(self):
        return self.__role
    
    def get_is_disabled(self):
        return self.__is_disabled

    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password
          
    def set_is_disabled(self, is_disabled):
        self.__is_disabled = is_disabled

    def login(self, input_password):
        return self.get_password() == input_password