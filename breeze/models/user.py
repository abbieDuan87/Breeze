class User:
    """The basic User class
    """
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__email = None # TODO: do we need email for register?
        
    def get_username(self):
        return self.__username
        
    def get_password(self):
        return self.__password
    
    def get_role(self):
        return self.__role
    
    def get_email(self):
        return self.__email

    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password
        
    def set_email(self, email):
        self.__email = email

    def login(self, input_password):
        return self.get_password() == input_password