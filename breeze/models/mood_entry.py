import uuid
from datetime import datetime

class MoodEntry:
    def __init__(self, mood, comment, date, time, mood_id=None):
        self.mood = mood
        self.comment = comment
        self.date = date
        self.time = time
        self.mood_id = str(uuid.uuid4()) if mood_id == None else mood_id

    def get_mood_id(self):
        return self.mood_id

    def get_mood(self):
        return self.mood

    def get_comment(self):
        return self.comment

    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def strip_comments(self):
        if len(self.comment) > 50:
            stripped = self.comment[:49]
            return stripped
        if  "\n" in self.comment:
            formatted = self.comment.replace("\n", "  ")
            return formatted
        return self.comment

    def to_dict(self):
        self.datetime = datetime.combine(self.date, self.time)
        return {
            'mood': self.mood,
            'comment': self.comment,
            'datetime': self.datetime
            }