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

def random_datetime(start, end):
    delta = end - start
    random_second = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_second)

def random_date_of_birth(min_age=18, max_age=80):
    today = datetime.now()
    birth_year = today.year - random.randint(min_age, max_age)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  # Avoid invalid dates
    return datetime(birth_year, birth_month, birth_day).strftime("%Y-%m-%d")

def generate_mood_entries(num_entries):
    moods = ["Very Happy", "Happy", "Neutral", "Sad", "Very Sad"]
    return [
        {
            "id": str(uuid.uuid4()),
            "mood": random.choice(moods),
            "comment": random.choice(["Feeling good.", "Tired.", "Stressed.", "Relaxed."]),
            "datetime": random_datetime_within_week().strftime("%Y-%m-%d %H:%M:%S"),
        }
        for _ in range(num_entries)
    ]

def generate_journals(num_entries):
    return [
        {
            "id": str(uuid.uuid4()),
            "title": f"Journal Entry {i + 1}",
            "text": "This is a journal entry text.",
            "date": random_datetime_within_week().strftime("%Y-%m-%d %H:%M:%S"),
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
            "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
            "notes": "Take with food.",
        }
    ]

def generate_appointments(patients, mhwps):
    statuses = ["requested", "confirmed", "cancelled"]
    appointments = []
    time_slots = [f"{hour}:{minute} {am_pm}" for hour in range(1, 13)
                  for minute in ["00", "30"] for am_pm in ["AM", "PM"]]

    for patient in patients:
        assigned_mhwp = patient["assignedMHWP"]
        if assigned_mhwp:
            num_appointments = random.randint(1, 3)  # Generate 1-3 appointments per patient
            for _ in range(num_appointments):
                appointment_date = random_datetime_within_week().strftime("%Y-%m-%d")
                appointment_time = random.choice(time_slots)

                appointment = {
                    "appointmentId": str(uuid.uuid4()),
                    "date": appointment_date,
                    "time": appointment_time,
                    "status": random.choice(statuses),
                    "mhwpUsername": assigned_mhwp,
                    "patientUsername": patient["username"],
                }

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
        patients.append({
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
            "moods": generate_mood_entries(random.randint(2, 5)),
            "journals": generate_journals(random.randint(1, 3)),
            "appointments": [],
            "conditions": generate_conditions(),
            "prescriptions": generate_prescriptions(),
        })
    return patients

def generate_mhwps(num_mhwps):
    mhwps = []
    for i in range(1, num_mhwps + 1):
        mhwp_username = f"mhwp{i}"
        mhwps.append({
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
        })
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