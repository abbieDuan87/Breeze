import json
from datetime import datetime
from breeze.models.admin import Admin
from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient
from breeze.models.appointment_entry import AppointmentEntry
from breeze.models.journal_entry import JournalEntry


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
            mood_entries=user_data.get("moods", []),
            journal_entries=user_data.get("journals", []),
            appointments=appointments,
            assigned_MHWP=user_data.get("assignedMHWP", None),
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

def retrieve_variables_from_data(filepath, username, variable):
    """Retrieves a list of variables (eg. all journal entries, mood entries) for a given user

    Args:
        filepath (str): Path to json file
        user (str): username to retrieve data for
        variable (str): variable which output will return

    Returns:
        list of dict: list of entries for given variable
    """
    with open (filepath, 'r') as file:
        data = json.load(file)
    for user in data['users']:
        if user['username'] == username:
            try:
                return user[variable]
            except KeyError:
                return list()
            
def save_attr_data(filepath, username, attribute, attribute_data):
    """Save edited attribute data (eg. journals, mood) to file

    Args:
        filepath (str): path to json
        username (str): username
        attribute (str): Attribute of interest
        attribute_data (list of dict): List of attributes
    """

    with open (filepath, 'r') as file:
        data = json.load(file)

    for user in data['users']:
        if user['username'] == username:
            user[attribute] = attribute_data
    
    with open (filepath, 'w') as file:
        json.dump(data, file, indent=4)

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
        appointment_entries.append(
            AppointmentEntry(
                date,
                time,
                status,
                mhwp_username,
                patient_username,
                appointment_id,
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
        title = entry.get("title")
        body = entry.get("entry")
        dt = entry.get("datetime")
        date = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").date()
        time = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").time()
        journal_entries.append(
            JournalEntry(
                title,
                body,
                date,
                time
            )
        )

    return journal_entries


# for testing, to run: python -m breeze.utils.data_utils
if __name__ == "__main__":
    users_data, appointments_data = load_data("./data/users.json")

    for username, user in users_data.items():
        print(f"User: {user.get_username()}")
        if user.get_appointments():
            for app in user.get_appointments():
                print(app)
