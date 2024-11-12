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
    
def direct_to_dashboard():
    print("\nPress B to go back:")
    while True:
        user_input = input("> ").strip().lower()
        if user_input == "b":
            break
        else:
            print("Invalid input. Please press B to go back.")