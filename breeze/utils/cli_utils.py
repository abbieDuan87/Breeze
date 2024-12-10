import os
import re
from datetime import datetime as dt
from breeze.utils.calendar_utils import get_colored_status, strip_ansi_codes

def print_system_message(message):
    """Print the system message in a box that dynamically sizes according to the length of the message.

    Args:
        message (str): the system message you want to display
    """
    lines = message.splitlines()

    max_width = max(len(strip_ansi_codes(line)) for line in lines) + 4
    print("-" * max_width)

    for line in lines:
        print(f"| {line.ljust(max_width - 4)} |")

    print("-" * max_width)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_disabled_account_dashboard_menu(username):
    """
    Prompts the user with a message when their account is disabled.

    Args:
        user (User): The user whose account is disabled.

    Returns:
        bool: True if the user chose to log out, otherwise False.
    """
    print_system_message(
        f"Hi {username}, your account has been disabled, please contact the admin for more info!"
    )
    print("[X] Log out")

    user_input = input("> ")
    if user_input.strip().lower() == "x":
        return True
    else:
        print_system_message(
            "Sorry, you can only log out because your account is disabled."
        )
        return False


def table_creator(headers, rows):
    column_widths = [
        max(len(strip_ansi_codes(str(row[i]))) for row in rows + [headers])
        for i in range(len(headers))
    ]

    separator = "+".join("-" * (width + 2) for width in column_widths)
    separator = f"+{separator}+"

    print(separator)
    print(
        "| "
        + " | ".join(
            header.center(width) for header, width in zip(headers, column_widths)
        )
        + " |"
    )
    print(separator)
    for row in rows:
        print(
            "| "
            + " | ".join(
                str(cell).ljust(
                    width + len(str(cell)) - len(strip_ansi_codes(str(cell)))
                )
                for cell, width in zip(row, column_widths)
            )
            + " |"
        )
    print(separator)


def print_appointments(appointments=[], is_own_view=True):
    if not appointments:
        print("No upcoming appointments.")
        return

    headers = ["#", "Date", "Time", "Status", "Patient", "MHWP"]

    rows = [
        [
            index + 1,
            app.date.strftime("%d-%m-%Y"),
            app.time,
            (
                get_colored_status(app.status)
                if is_own_view
                else (
                    get_colored_status("unavailable")
                    if app.status == "confirmed"
                    else get_colored_status(app.status)
                )
            ),
            app.patient_username,
            app.mhwp_username,
        ]
        for index, app in enumerate(appointments)
    ]

    table_creator(headers, rows)


def print_user_appointments(appointments=[], page=1):
    if not appointments:
        return
    lower = (page - 1) * 10
    if len(appointments) > ((page - 1) * 10 + 10):
        upper = lower + 10
        page_data = appointments[::-1][lower:upper]
    elif len(appointments) > ((page - 1) * 10):
        page_data = appointments[::-1][lower:]
    else:
        print("No appointments on this page!")
        return False

    headers = ["#", "MHWP", "Appointment Summary", "Date", "Time"]

    rows = []
    no_rows = 1
    for appt in page_data:
        if appt.summary == None:
            continue
        else:
            stripped = appt.strip_summary()
            rows.append(
                [
                    no_rows,
                    appt.mhwp_username,
                    stripped,
                    appt.date,
                    appt.time,
                ]
            )
            no_rows += 1
    table_creator(headers, rows)

    return True


def print_journals(journal_data=[], page=1):
    if not journal_data:
        return
    lower = (page - 1) * 10
    if len(journal_data) > ((page - 1) * 10 + 10):
        upper = lower + 10
        page_data = journal_data[::-1][lower:upper]
    elif len(journal_data) > ((page - 1) * 10):
        page_data = journal_data[::-1][lower:]
    else:
        print("No journal items on this page!")
        return False

    headers = ["#", "Title", "Text", "Date", "Time", "Last Update"]

    rows = []
    for index, entry in enumerate(page_data):
        title = entry.strip_title()
        stripped = entry.strip_entry()
        date_time = entry.date + ' ' + entry.time
        rows.append(
            [
                index + 1,
                title,
                stripped,
                entry.date,
                entry.time,
                entry.last_update if str(entry.last_update) != str(date_time) else 'No Updates'
            ]
        )
    table_creator(headers, rows)
    return True


def print_moods(mood_data=[], page=1):
    mood_colouring = {
        "G": {
            "name": "Green",
            "description": "Very Happy",
            "color_code": 40,
            "emoji": "\U0001F60A",
        },
        "L": {
            "name": "Light Green",
            "description": "Happy",
            "color_code": 120,
            "emoji": "\U0001F642",
        },
        "Y": {
            "name": "Yellow",
            "description": "Neutral",
            "color_code": 226,
            "emoji": "\U0001F610",
        },
        "O": {
            "name": "Orange",
            "description": "Sad",
            "color_code": 208,
            "emoji": "\U0001F641",
        },
        "R": {
            "name": "Red",
            "description": "Very Sad",
            "color_code": 160,
            "emoji": "\U0001F622",
        },
    }
    if not mood_data:
        return
    lower = (page - 1) * 10
    if len(mood_data) > ((page - 1) * 10 + 10):
        upper = lower + 10
        page_data = mood_data[::-1][lower:upper]
    elif len(mood_data) > ((page - 1) * 10):
        page_data = mood_data[::-1][lower:]
    else:
        print("No journal items on this page!")
        return False

    headers = ["#", "Mood", "Comment", "Date", "Time"]

    rows = []
    for index, mood in enumerate(page_data):
        comment = mood.strip_comments()
        rows.append(
            [
                index + 1,
                mood.mood,
                comment,
                mood.date,
                mood.time,
            ]
        )

    table_creator(headers, rows)
    return True


def is_empty(input):
    if not input:
        print_system_message("Field cannot be empty. Please try again.")
        return True


def is_valid_name(name):
    if len(name) == 1 and name.isalpha() == False:
        print_system_message(
            "Name must be longer than one character and contain only alphabetic characters. Please try again."
        )
        return False
    elif len(name) == 1:
        print_system_message(
            "Name must be longer than one character. Please try again."
        )
        return False
    for i in name:
        if i.isalpha() == False:
            print_system_message("Name cannot contain non-alphabetic characters.")
            return False
    return True


def is_invalid_username(username, users):
    if username in users:
        print_system_message("Username already taken! Please choose another.")
        return True
    elif username.lower() != username or len(username) < 2 or len(username) > 10:
        print_system_message(
            "Username must be in lowercase and be between two and ten characters! Please try again."
        )
        return True
    elif len(username.split(" ")) > 1:
        print_system_message("Username cannot include spaces! Please try again.")
        return True
    else:
        return False


def is_invalid_date(date):
    date_regex = "^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-([0-9]{4})$"
    if re.match(date_regex, date):
        # secondary check for invalid dates eg. 31 Sep, 31 Feb
        try:
            dob_check = dt.strptime(date, "%d-%m-%Y")
            sixteenth = dt(dob_check.year + 16, dob_check.month, dob_check.day)
            if dt.now() > sixteenth:
                return False
            else:
                print_system_message("You must be over 16 to use the Breeze service!")
                return True
        except ValueError:
            print_system_message(
                "Date is invalid! Please enter a existing date of birth."
            )
            return True
    else:
        print_system_message("Date is incorrectly formulated! Please try again.")
        return True


def is_invalid_email(email):
    email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if email != "":
        if re.match(email_regex, email):
            return False
        else:
            print_system_message("Email is formatted incorrectly! Please try again.")
            return True


def clear_screen_and_show_banner(banner_str):
    clear_screen()
    print(banner_str)


def check_exit(input_value):
    if input_value.strip().lower() == "x":
        return True
    return False


def check_previous(input_value):
    if input_value.strip().lower() == "r":
        return True
    return False


def direct_to_dashboard(message=""):
    if message:
        print(f"\n{message}")
    print("Please press [B] to go back to the dashboard.")

    while True:
        user_input = input("> ").strip().lower()
        if user_input == "b":
            clear_screen()
            break
        else:
            print("Invalid input. Please press [B] to go back to the dashboard.")
