class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def login(self, input_password):
        return self.password == input_password