import datetime as dt
import uuid 

class JournalEntry:
    def __init__(self, title, entry, date, time, journal_id=None, last_update=None):
        self.journal_id = str(uuid.uuid4()) if journal_id == None else journal_id
        self.title = title
        self.entry = entry
        self.date = date
        self.time = time
        time_dt = time
        date_dt = date
        if type(date) == str:
            date_dt = dt.datetime.strptime(date, "%Y-%m-%d").date()
        if type(time) == str:
            time_dt = dt.datetime.strptime(time, "%H:%M:%S").time()
        self.last_update = last_update if last_update else dt.datetime.combine(date_dt, time_dt)

    def get_id(self):
        return self.journal_id

    def get_title(self):
        return self.title
    
    def get_entry(self):
        return self.entry
    
    def set_title(self, title):
        self.title = title
    
    def set_entry(self, entry):
        self.entry = entry
    
    def get_date(self):
        return self.date

    def get_time(self):
        return self.time 

    def get_update(self):
        return self.last_update

    def set_update(self):
        self.last_update = dt.datetime.now() 
      
    def to_dict(self):
        datetime = dt.datetime.combine(self.date, self.time)
        return {
            'id' : self.journal_id,
            'title' : self.title,
            'entry' : self.entry,
            'date' : datetime
        }
    
    def strip_title(self):
        if len(self.title) > 20:
            stripped_title = self.title[:19] + '...'
            return stripped_title
        else:
            return self.title
        
    def strip_entry(self):
        if len(self.entry) > 50:
            stripped_entry = self.entry[:49] + '...'
            return stripped_entry
        else:
            return self.entry
    
    def __str__(self):
        return (
            f"JournalEntry(\n"
            f"  title={self.title},\n"
            f"  text={self.entry}"
            f"  date={self.date},\n"
            f"  time={self.time},\n"
            f")"
        )
    