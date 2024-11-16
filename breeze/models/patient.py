from .user import User

class Patient(User):
    def __init__(self, username, password, first_name = None, last_name = None, email=None, emergency_contact_email=None, is_disabled=False, mood_entries=[], journal_entries=[], appointments=[]):
        super().__init__(username, password, role="Patient", is_disabled=is_disabled)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email 
        self.__emergency_contact_email = emergency_contact_email
        self.__mood_entries = mood_entries
        self.__journal_entries = journal_entries
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
    
    def get_emergency_contact(self):
        return self.__emergency_contact_email
    
    def set_emergency_contact(self, email):
        self.__emergency_contact_email = email
    
    def get_mood_entries(self):
        return self.__mood_entries
    
    def set_appointments(self, appointments): 
        self.__appointments = appointments
    
    def add_mood_entry(self, mood, comment, datetime):
        self.__mood_entries.append({"mood": mood, "comment": comment, "datetime": datetime})
    
    def add_journal_entry(self, entry, datetime):
        self.__journal_entries.append({"entry": entry, "datetime": datetime})
    
    def __str__(self):
        return f"Patient: {self.get_username()}, Role: {self.get_role()}"
    
    def __repr__(self):
        return f"Patient(username={self.get_username()}, role={self.get_role()})"
    
    def to_dict(self):
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "role": self.get_role(),
            "isDisabled": self.get_is_disabled(),
            "information": {
                "firstName": self.get_first_name(),
                "lastName": self.get_last_name(),
                "email": self.get_email(),
                "emergencyContactEmail": self.get_emergency_contact()  
            },
            "moods": self.__mood_entries,
            "journals": self.__journal_entries,
            "appointments": self.__appointments
        }