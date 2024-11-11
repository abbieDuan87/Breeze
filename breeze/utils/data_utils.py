import json

from breeze.models.admin import Admin
from breeze.models.mhwp import MHWP
from breeze.models.patient import Patient

def decode_user(user_data):
    """
    Decodes a dictionary of user data into the appropriate user object (Patient, Admin, MHWP).

    Args:
        user_data (dict): User data containing 'username', 'password', 'role', etc.

    Returns:
        User: An instance of Patient, Admin, or MHWP based on the 'role' field. 
              Returns the original data if the role is unrecognized.
    """
    role = user_data.get("role", "").lower()
    
    if role == "patient":
        return Patient(
            username=user_data.get("username"),
            password=user_data.get("password"),
            is_disabled=user_data.get("isDisabled", False),
            mood_entries=user_data.get("moods", []),
            journal_entries=user_data.get("journals", []),
            appointments=user_data.get("appointments", [])
        )

    elif role == "admin":
         return Admin(
            username=user_data.get("username"),
            password=user_data.get("password"),
            is_disabled=user_data.get("isDisabled", False)
        )
    
    elif role == "mhwp":
        return MHWP(
            username=user_data.get("username"),
            password=user_data.get("password"),
            is_disabled=user_data.get("isDisabled", False),
            appointments=user_data.get("appointments", [])
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
            return json.load(file, object_hook=decode_user)
    except FileNotFoundError:
        return {}

def save_data(file_path, data):
    """
    Saves data to a JSON file.

    Args:
        file_path (str): Path to the file.
        data (dict): Data to save, usually a dictionary or list.

    Returns:
        None
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# for testing, to run: python -m breeze.utils.data_utils
if __name__ == "__main__":
    data = load_data('./data/users.json')
    users = data.get("users", [])
    
    for user in users:
        print(user)
    