from .user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="Admin")