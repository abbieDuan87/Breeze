import os

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
    os.system('cls' if os.name == 'nt' else 'clear')
    
def show_disabled_account_dashboard_menu(username):
    """
    Prompts the user with a message when their account is disabled.
    
    Args:
        user (User): The user whose account is disabled.
        
    Returns:
        bool: True if the user chose to log out, otherwise False.
    """
    print_system_message(f'Hi {username}, your account has been disabled, please contact the admin for more info!')
    print("[X] Log out")
            
    user_input = input('> ')
    if user_input.strip().lower() == "x":
        return True
    else:
        print_system_message("Sorry, you can only log out because your account is disabled.")
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