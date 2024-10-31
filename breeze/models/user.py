class User:
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role
        
    def get_password(self):
        return self.__password

    def login(self, input_password):
        return self.get_password() == input_password