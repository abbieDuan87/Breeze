import datetime


def get_next_available_days(num_days=5):
    """Returns a list of the next available weekdays, excluding weekends.

    Args:
        num_days (int, optional): The number of weekdays to retrieve. Defaults to 5.

    Returns:
        list of datetime.date: A list of dates representing the next available weekdays.
    """
    available_days = []
    today = datetime.date.today()
    days_count = 0

    while days_count < num_days:
        today += datetime.timedelta(days=1)
        if today.weekday() < 5:
            available_days.append(today)
            days_count += 1

    return available_days


def generate_time_slots(start="09:00", end="17:00", interval_minutes=30):
    """
    Generete time slot from start time to end time with certain interval.
    Args:
        start (str, optional): . Defaults to "09:00".
        end (str, optional): . Defaults to "17:00".
        interval_minutes (int, optional): . Defaults to 30.

    Returns:
        str[]: a list of str, of the time slots
    """
    start_time = datetime.datetime.strptime(start, "%H:%M")
    end_time = datetime.datetime.strptime(end, "%H:%M")
    slots = []

    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime("%I:%M %p"))
        current_time += datetime.timedelta(minutes=interval_minutes)

    return slots


def generate_calendar_slot_code_map(next_available_days, time_slots):
    """Generates a dictionary mapping unique codes to (date, time) pairs.

    Args:
        next_available_days (list): List of upcoming weekdays.
        time_slots (list): List of time slots for each day.

    Returns:
        dict: A dictionary where each key is a code (e.g., "A1") and each value is a (date, time) tuple.
    """
    codes = {}
    for i, slot in enumerate(time_slots):
        col_code = chr(ord("A") + i)
        for j, day in enumerate(next_available_days):
            row_code = j + 1
            codes[f"{col_code}{row_code}"] = (day, slot)
    return codes


if __name__ == "__main__":
    days = get_next_available_days()
    slots = generate_time_slots()
    codes = generate_calendar_slot_code_map(days, slots)
    print(codes)
    print(len(slots))
