from .user import User

class Patient(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="Patient")
        self.mood_entries = []
        self.journal_entries = []

    def add_mood_entry(self, mood, comment):
        self.mood_entries.append({"mood": mood, "comment": comment})
    
    def add_journal_entry(self, entry):
        self.journal_entries.append({"entry": entry})