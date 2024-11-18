from .user import User

class Admin(User):
    def __init__(self, username, password, is_disabled=False):
        super().__init__(username, password, role="Admin", is_disabled=is_disabled)
    
    def __str__(self):
        return f"Admin: {self.get_username()}, Role: {self.get_role()}"
    
    def __repr__(self):
        return f"Admin(username={self.get_username()}, role={self.get_role()})"
    
    def to_dict(self):
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "role": self.get_role(),
            "isDisabled": self.get_is_disabled(),
        }