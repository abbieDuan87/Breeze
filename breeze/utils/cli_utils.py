import os

from breeze.utils.calendar_utils import get_colored_status, strip_ansi_codes


def print_system_message(message):
    """Print the system message in a box that dynamically sizes according to the length of the message.

    Args:
        message (str): the system message you want to display
    """
    lines = message.splitlines()

    # Determine the maximum width based on the longest line
    max_width = max(len(line) for line in lines) + 4  # 4 for padding and borders

    print("-" * max_width)

    # Print each line with padding
    for line in lines:
        print(f"| {line.ljust(max_width - 4)} |")  # Align text to the left with padding

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


def direct_to_dashboard(message=""):
    """
    Helper function to return to the dashboard with a custom message.

    Args:
        message (str): Custom message to display before the prompt.
    """
    if message:
        print(f"\n{message}")
    print("Please press B to go back to the dashboard.")

    while True:
        user_input = input("> ").strip().lower()
        if user_input == "b":
            clear_screen()
            break
        else:
            print("Invalid input. Please press B to go back to the dashboard.")


def return_to_previous(string, param):
    if string.strip().lower() == param:
        return True


def print_appointments(appointments=[]):
    if not appointments:
        print("No upcoming appointments.")
        return

    headers = ["#", "Date", "Time", "Status", "Patient", "MHWP"]

    rows = [
        [
            index + 1,
            app.date,
            app.time,
            get_colored_status(app.status),
            app.patient_username,
            app.mhwp_username,
        ]
        for index, app in enumerate(appointments)
    ]

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
                str(cell).ljust(width + len(str(cell)) - len(strip_ansi_codes(str(cell))))
                for cell, width in zip(row, column_widths)
            )
            + " |"
        )
    print(separator)


def clear_screen_and_show_banner(banner_str):
    clear_screen()
    print(banner_str)
