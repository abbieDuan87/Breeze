import json
from datetime import datetime
from breeze.models.admin import Admin
from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.models.appointment_entry import AppointmentEntry
from breeze.models.journal_entry import JournalEntry
from breeze.models.mood_entry import MoodEntry


def decode_user(user_data, appointments_data):
    """
    Decodes a dictionary of user data into the appropriate user object (Patient, Admin, MHWP).

    Args:
        user_data (dict): User data containing 'username', 'password', 'role', etc.
        appointments_data (dict): Dictionary of all appointments.

    Returns:
        User: An instance of Patient, Admin, or MHWP based on the 'role' field.
              Returns the original data if the role is unrecognized.
    """
    role = user_data.get("role", "").lower()

    # Get the list of appointment_ids and retrieve actual AppointmentEntry objects
    appointment_ids = user_data.get("appointments", [])
    appointments = [
        appointments_data.get(app_id)
        for app_id in appointment_ids
        if appointments_data.get(app_id)
    ]

    if role == "patient":
        return Patient(
            username=user_data.get("username"),
            password=user_data.get("password"),
            is_disabled=user_data.get("isDisabled", False),
            first_name=user_data.get("information", {}).get("firstName"),
            last_name=user_data.get("information", {}).get("lastName"),
            email=user_data.get("information", {}).get("email"),
            emergency_contact_email=user_data.get("information", {}).get(
                "emergencyContactEmail"
            ),
            gender=user_data.get("information", {}).get("gender"),
            date_of_birth=user_data.get("information", {}).get("dateOfBirth"),
            mood_entries=user_data.get("moods", []),
            journal_entries=user_data.get("journals", []),
            appointments=appointments,
            assigned_MHWP=user_data.get("assignedMHWP", None),
            conditions=user_data.get("conditions", {}),
            prescriptions=user_data.get("prescriptions", []),
        )

    elif role == "admin":
        return Admin(
            username=user_data.get("username"),
            password=user_data.get("password"),
            first_name=user_data.get("information", {}).get("firstName"),
            last_name=user_data.get("information", {}).get("lastName"),
            email=user_data.get("information", {}).get("email"),
            is_disabled=user_data.get("isDisabled", False),
        )

    elif role == "mhwp":
        return MHWP(
            username=user_data.get("username"),
            password=user_data.get("password"),
            first_name=user_data.get("information", {}).get("firstName"),
            last_name=user_data.get("information", {}).get("lastName"),
            email=user_data.get("information", {}).get("email"),
            is_disabled=user_data.get("isDisabled", False),
            appointments=appointments,
            assigned_patients=user_data.get("assignedPatients", []),
        )

    return user_data


def load_data(file_path):
    """
    Loads and decodes user data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Decoded user data as a dictionary of user objects. Returns an empty dictionary if the file is not found.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            appointment_entries = create_appointments_from_data(
                data.get("appointments", [])
            )

            appointments_data = {
                appointment.get_id(): appointment for appointment in appointment_entries
            }

            users = data.get("users", [])
            user_objects = {}
            for user in users:
                user_objects[user["username"]] = decode_user(user, appointments_data)

            return user_objects, appointments_data

    except FileNotFoundError:
        return {}, {}


def save_data(file_path, user_object_list):
    """
    Saves data to a JSON file.

    Args:
        file_path (str): Path to the file.
        data (dict): Data to save, usually a dictionary or list.

    Returns:
        None
    """
    unique_appointments = {}

    for user in user_object_list:
        if user.get_role().lower() != "admin":
            for app in user.get_appointments():
                unique_appointments[app.get_id()] = app

    appointments_dict_list = [app.to_dict() for app in unique_appointments.values()]
    users_dict_list = [user.to_dict() for user in user_object_list]

    data_to_save = {"appointments": appointments_dict_list, "users": users_dict_list}

    with open(file_path, "w") as file:
        json.dump(data_to_save, file, indent=4)

        
def create_appointments_from_data(appointments_data):
    """Convert each appointment entry (dictionary) into Appoinment Entry object

    Args:
        appointments_data (list of dict): _description_

    Returns:
        list of AppointmentEntry: _description_
    """
    appointment_entries = []

    for app in appointments_data:
        date = app.get("date")
        time = app.get("time")
        status = app.get("status", None)
        mhwp_username = app.get("mhwpUsername", None)
        patient_username = app.get("patientUsername", None)
        appointment_id = app.get("appointmentId", None)
        summary = app.get("summary", None)
        appointment_entries.append(
            AppointmentEntry(
                date,
                time,
                status,
                mhwp_username,
                patient_username,
                appointment_id,
                summary,
            )
        )

    return appointment_entries


def create_journal_entries_from_data(journal_data):
    """Convert each journal entry (dictionary) into JournalEntry object

    Args:
       journal_data (list of dict): User specific list of journals

    Returns:
        journal_entries: JournalEntry objects
    """
    journal_entries = []

    for entry in journal_data:
        journal_id = entry.get("id")
        title = entry.get("title")
        body = entry.get("text")
        dt = entry.get("date")
        last_update = entry.get("last_update")
        date = dt[:10]
        time = dt[11:]
        journal_entries.append(
            JournalEntry(
                title,
                body,
                date,
                time,
                journal_id=journal_id,
                last_update=last_update
            )
        )

    return journal_entries


def create_mood_entries_from_data(mood_data):
    """Convert each mood entry (dictionary) into MoodEntry object

    Args:
       mood_data (list of dict): User specific list of moods

    Returns:
        list of MoodEntry objects
    """
    mood_entries = []

    for entry in mood_data:
        mood_id = entry.get("id")
        mood = entry.get("mood")
        comment = entry.get("comment")
        dt = entry.get("date")
        date = datetime.strptime(dt, "%d-%m-%Y %H:%M:%S").date()
        time = datetime.strptime(dt, "%d-%m-%Y %H:%M:%S").time()
        mood_entries.append(
            MoodEntry(
                mood,
                comment,
                date,
                time,
                mood_id=mood_id
            )
        )

    return mood_entries


# for testing, to run: python -m breeze.utils.data_utils
if __name__ == "__main__":
    users_data, appointments_data = load_data("./data/users.json")

    for username, user in users_data.items():
        print(f"User: {user.get_username()}")
        if user.get_appointments():
            for app in user.get_appointments():
                print(app)
