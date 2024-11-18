class appointmentEntry:
    
    def __init__(self, date, time, isCancelled):
        self.isCancelled = isCancelled
        self.date = date
        self.time = time 

    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def is_cancelled(self):  
        return self.isCancelled
    
    def cancel_appointment(self):
        self.isCancelled = True 