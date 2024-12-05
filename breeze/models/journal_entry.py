import datetime as dt
import uuid 

class JournalEntry:
    def __init__(self, title, entry, date, time, journal_id=None):
        self.journal_id = str(uuid.uuid4()) if journal_id == None else journal_id
        self.title = title
        self.entry = entry
        self.date = date
        self.time = time

    def get_id(self):
        return self.journal_id

    def get_title(self):
        return self.title
    
    def get_entry(self):
        return self.entry
    
    def get_date(self):
        return self.date

    def get_time(self):
        return self.time  
      
    def to_dict(self):
        datetime = dt.datetime.combine(self.date, self.time)
        return {
            'id' : self.journal_id,
            'title' : self.title,
            'entry' : self.entry,
            'datetime' : datetime
        }
    
    def strip_title(self):
        stripped = self.title
        if "\n" in stripped:
            stripped = stripped.replace("\n", "  ")
        if len(self.summary) > 20:
            stripped = stripped[:19] + '...'
        return stripped
        
    def strip_entry(self):
        stripped = self.entry
        if "\n" in stripped:
            stripped = stripped.replace("\n", "  ")
        if len(stripped) > 50:
            stripped = stripped[:50] + '...'
        return stripped
    
    def __str__(self):
        return (
            f"JournalEntry(\n"
            f"  title={self.title},\n"
            f"  entry={self.entry}"
            f"  date={self.date},\n"
            f"  time={self.time},\n"
            f")"
        )
    