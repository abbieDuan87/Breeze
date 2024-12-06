import os
import json
import random
import uuid
from datetime import datetime, timedelta


def random_datetime_within_week():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return random_datetime(start_of_week, end_of_week)


def random_datetime_next_weekdays():
    today = datetime.now()

    weekdays = [today]
    for i in range(1, 6):
        next_day = today + timedelta(days=i)
        if next_day.weekday() == 5:
            next_day += timedelta(days=2)
        elif next_day.weekday() == 6:
            next_day += timedelta(days=1)
        weekdays.append(next_day)

    random_weekday = random.choice(weekdays)
    return random_weekday


def random_datetime_next_last(next_last):
    dates = []
    j = 1 if next_last == "next" else -1
    for i in range(7):
        if next_last == "last":
            i += 1
        last_day = (datetime.now() + timedelta(days=i * j)).date()
        if last_day.weekday() in (5, 6):
            continue
        else:
            dates.append(last_day)
    return random.choice(dates)

  
def random_datetime(start, end):
    delta = end - start
    random_second = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_second)


def random_date_of_birth(min_age=18, max_age=80):
    today = datetime.now()
    birth_year = today.year - random.randint(min_age, max_age)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  # Avoid invalid dates
    return datetime(birth_year, birth_month, birth_day).strftime("%d-%m-%Y")


def generate_mood_entries(num_entries):
    moods = {
        "Very Happy" : [":D", "Feeling awesome!", "Love this feeling!"], 
        "Happy" : [":)", "Feel good.", "Life is good."],
        "Neutral" : ["Feeling alright.", ":|", "It is what it is."], 
        "Sad": ["Feeling bad.", "Feeling a bit down.", ":/"], 
        "Very Sad": ["Feel terrible.", "Feeling awful right now.", ":("]}
    
    dates = [random_datetime_within_week().strftime("%d-%m-%Y %H:%M:%S") for i in range(num_entries)]
    dates = sorted(dates)
    moods_list = [random.choice(list(moods.keys())) for i in range(num_entries)]
    return [
        {
            "id": str(uuid.uuid4()),
            "mood": moods_list[i-1],
            "comment": random.choice(moods[moods_list[i-1]]),
            "date": dates[i],
        }
        for i in range(num_entries)
    ]


def generate_journals(num_entries):
    dates = [random_datetime_within_week().strftime("%d-%m-%Y %H:%M:%S") for i in range(num_entries)]
    dates = sorted(dates)
    journal_texts = [
        "Today was amazing! I felt so accomplished after finishing my project. Everything just clicked.",
        "I had a rough day. It feels like nothing I do is enough, and it's weighing on me.",
        "What a peaceful afternoon. I went for a walk and just enjoyed the fresh air and sunshine.",
        "Everything went wrong today. Missed the bus, spilled coffee, and got stuck in traffic. Feeling exhausted.",
        "Spent the evening with friends, laughing and sharing stories. My heart feels full of joy.",
        "Feeling lonely tonight. Even surrounded by people, I can't shake this sense of isolation.",
        "Had a productive day at work. Checked off all my tasks and even got a compliment from my boss.",
        "Woke up with a sense of dread that just wouldn’t go away. It's like a cloud hovering over me all day.",
        "Cooked a new recipe today and nailed it! Small wins like this make me happy.",
        "Dealt with a disagreement with a close friend. I hate conflict—it leaves me feeling unsettled."
        "Had the most incredible workout today. I feel so energized and proud of myself for sticking with it!",
        "Today felt overwhelming. There were so many tasks to do, and I barely made it through.",
        "I had a quiet day at home, but it was nice to recharge and enjoy my own company.",
        "The sadness hit me hard this evening. It's tough when memories resurface out of nowhere.",
        "Got an unexpected compliment from a stranger today. It really made my day brighter.",
        "I feel stuck in a rut right now. Everything feels repetitive, and I don’t know how to break free.",
        "Spent some quality time with family today. It was heartwarming to reminisce about old times.",
        "Had to make a tough decision at work. I'm second-guessing myself, and it's stressing me out.",
        "Tried meditating for the first time today. It was calming and gave me a sense of peace I didn’t expect.",
        "The day started fine but ended on a sour note. A mistake I made came back to haunt me."
    ]

    return [
        {
            "id": str(uuid.uuid4()),
            "title": f"Journal Entry {i + 1}",
            "text": random.choice(journal_texts),
            "date": dates[i],
            "last_update": dates[i]
        }
        for i in range(num_entries)
    ]


def generate_conditions():
    conditions = ["Anxiety", "Depression", "PTSD", "Bipolar Disorder"]
    return {
        random.choice(conditions): [
            {
                "note": f"Details about {random.choice(conditions)}.",
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        ]
    }


def generate_prescriptions():
    medications = ["Sertraline", "Fluoxetine", "Clonazepam", "Paracetamol"]
    return [
        {
            "medication": random.choice(medications),
            "dosage": f"{random.randint(1, 3)} mg",
            "frequency": "once daily",
            "start_date": (datetime.now() - timedelta(days=30)).strftime("%d-%m-%Y"),
            "end_date": (datetime.now() + timedelta(days=180)).strftime("%d-%m-%Y"),
            "notes": "Take with food.",
        }
    ]


def generate_appointments(patients, mhwps):
    statuses = ["requested", "confirmed", "cancelled"]
    summaries = [
        "Discussed coping strategies for anxiety, set goals.",
        "Reviewed sleep habits; introduced mindfulness exercises.",
        "Explored stress triggers; created a relaxation plan.",
        "Focused on emotional regulation; reviewed progress.",
        "Addressed work-life balance challenges; set boundaries.",
        "Discussed past trauma and initiated processing therapy.",
        "Worked on social anxiety; practiced exposure techniques.",
        "Identified cognitive distortions; introduced CBT tools.",
        "Explored grief and coping strategies for loss.",
        "Focused on self-esteem building activities and affirmations.",
        "Reviewed progress on anger management techniques.",
        "Introduced journaling as a tool for emotional expression.",
        "Worked on communication skills in relationships.",
        "Explored values and goal alignment in life planning.",
        "Discussed medication effects; adjusted treatment plan.",
        "Processed recent life changes; emphasized resilience.",
        "Focused on grounding techniques for managing panic.",
        "Explored triggers for depression; planned positive activities.",
        "Reviewed progress with therapy goals and setbacks.",
        "Addressed guilt and worked on self-forgiveness strategies.",
    ]

    appointments = []
    time_slots = []
    for hour in range(9, 17):
        for minute in ["00", "30"]:
            am_pm = "AM" if hour < 12 else "PM"

            display_hour = hour if hour <= 12 else hour - 12
            display_hour = 12 if hour == 12 else display_hour

            time_slots.append(f"{display_hour}:{minute} {am_pm}")

    for patient in patients:
        assigned_mhwp = patient["assignedMHWP"]
        if assigned_mhwp:
            for i in range(2):
                # generate elapsed appointments first
                next_last = "last" if i == 0 else "next"
                num_appointments = random.randint(
                    1, 3
                )  # Generate 1-3 appointments per patient
                generated_appointments = set()  # prevent generated overlap appointment
                for _ in range(num_appointments):
                    appointment_date = random_datetime_next_last(next_last).strftime(
                        "%d-%m-%Y"
                    )
                    appointment_time = random.choice(time_slots)

                    appointment_key = (appointment_date, appointment_time)

                    if appointment_key in generated_appointments:
                        break
                    else:
                        generated_appointments.add(appointment_key)

                    appointment = {
                        "appointmentId": str(uuid.uuid4()),
                        "date": appointment_date,
                        "time": appointment_time,
                        "status": random.choice(statuses) if i == 1 else "confirmed",
                        "mhwpUsername": assigned_mhwp,
                        "patientUsername": patient["username"],
                    }

                    # Add comment if appointment was in the past
                    if i == 0:
                        appointment["summary"] = random.choice(summaries)

                    # Add the appointment to the global list
                    appointments.append(appointment)

                    # Link the appointment ID to the patient
                    if "appointments" not in patient:
                        patient["appointments"] = []
                    patient["appointments"].append(appointment["appointmentId"])

                    # Link the appointment ID to the assigned MHWP
                    for mhwp in mhwps:
                        if mhwp["username"] == assigned_mhwp:
                            if "appointments" not in mhwp:
                                mhwp["appointments"] = []
                            mhwp["appointments"].append(appointment["appointmentId"])
                            break

    return appointments


def generate_patients(num_patients, mhwp_usernames):
    genders = ["Male", "Female", "Non-binary", "Other"]
    patients = []
    for i in range(1, num_patients + 1):
        assigned_mhwp = mhwp_usernames[(i - 1) % len(mhwp_usernames)]
        patients.append(
            {
                "username": f"patient{i}",
                "password": "",
                "role": "Patient",
                "isDisabled": False,
                "information": {
                    "firstName": f"Patient{i}First",
                    "lastName": f"Patient{i}Last",
                    "email": f"patient{i}@example.com",
                    "emergencyContactEmail": f"emergency.patient{i}@example.com",
                    "gender": random.choice(genders),
                    "dateOfBirth": random_date_of_birth(),
                },
                "assignedMHWP": assigned_mhwp,
                "moods": generate_mood_entries(random.randint(2, 15)),
                "journals": generate_journals(random.randint(1, 5)),
                "appointments": [],
                "conditions": generate_conditions(),
                "prescriptions": generate_prescriptions(),
            }
        )
    return patients


def generate_mhwps(num_mhwps):
    mhwps = []
    for i in range(1, num_mhwps + 1):
        mhwp_username = f"mhwp{i}"
        mhwps.append(
            {
                "username": mhwp_username,
                "password": "",
                "role": "MHWP",
                "isDisabled": False,
                "information": {
                    "firstName": f"MHWP{i}First",
                    "lastName": f"MHWP{i}Last",
                    "email": f"mhwp{i}@example.com",
                },
                "appointments": [],
                "assignedPatients": [],
            }
        )
    return mhwps


def generate_admin():
    return {
        "username": "admin",
        "password": "",
        "role": "Admin",
        "isDisabled": False,
        "information": {
            "firstName": "Admin",
            "lastName": "User",
            "email": "admin@example.com",
        },
    }


def main():
    num_patients = 10
    num_mhwps = 3

    mhwps = generate_mhwps(num_mhwps)
    patients = generate_patients(num_patients, [mhwp["username"] for mhwp in mhwps])
    appointments = generate_appointments(patients, mhwps)

    for patient in patients:
        assigned_mhwp = patient["assignedMHWP"]
        for mhwp in mhwps:
            if mhwp["username"] == assigned_mhwp:
                mhwp["assignedPatients"].append(patient["username"])

    users = patients + mhwps + [generate_admin()]

    data = {
        "appointments": appointments,
        "users": users,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/users.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Dummy data has been generated and saved to 'data/users.json'.")


if __name__ == "__main__":
    main()
