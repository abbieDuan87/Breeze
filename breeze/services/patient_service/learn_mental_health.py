from breeze.utils.cli_utils import (
    clear_screen,
    print_system_message,
    direct_to_dashboard,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def learn_mental_health():
    # Data
    MENTAL_HEALTH_RESOURCES = {
        "1": {
            "name": "Anxiety",
            "summary": "Anxiety is a feeling of unease, such as worry or fear, that can be mild or severe.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/anxiety/"]
        },
        "2": {
            "name": "Depression",
            "summary": "Depression is a low mood that lasts a long time and affects your daily life.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/clinical-depression/"]
        },
        "3": {
            "name": "Stress",
            "summary": "Stress is the body's reaction to feeling threatened or under pressure.",
            "resources": ["https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/"]
        },
        "4": {
            "name": "PTSD (Post-Traumatic Stress Disorder)",
            "summary": "PTSD is a mental health condition triggered by a terrifying event.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/post-traumatic-stress-disorder-ptsd/"]
        },
        "5": {
            "name": "OCD (Obsessive-Compulsive Disorder)",
            "summary": "OCD is a common mental health condition where a person has obsessive thoughts and compulsive behaviours.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/obsessive-compulsive-disorder-ocd/"]
        },
        "6": {
            "name": "Bipolar Disorder",
            "summary": "Bipolar disorder is characterised by extreme mood swings, including emotional highs and lows.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/bipolar-disorder/"]
        },
        "7": {
            "name": "Eating Disorders",
            "summary": "Eating disorders involve unhealthy eating behaviours and can affect mental and physical health.",
            "resources": ["https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/eating-disorders/overview/"]
        },
        "8": {
            "name": "Phobias",
            "summary": "A phobia is an overwhelming and debilitating fear of an object, place, situation, feeling or animal.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/phobias/overview/"]

        },
        "9": {
            "name": "Panic disorder",
            "summary": "Panic disorder is an anxiety disorder where you regularly have sudden attacks of panic or fear.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/panic-disorder/"]

        },
        "10": {
            "name": "Antisocial personality disorder (ASPD)",
            "summary": "Personality disorders are mental health conditions that affect how someone thinks, perceives, feels or relates to others.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/antisocial-personality-disorder/"]

        },
        "u": {
            "name": "Useful Resources",
            "summary": "General resources to support mental health and well-being.",
            "resources": [
                "https://www.nhs.uk/mental-health/",
                "https://www.nhs.uk/every-mind-matters/",
                "https://www.nhs.uk/mental-health/self-help/",
                "https://www.nhs.uk/conditions/stress-anxiety-depression/mental-health-helplines/"
            ]
        }
    }

    while True:
        clear_screen()
        print(PATIENT_BANNER_STRING)
        print("Learn More About Mental Health Conditions and Useful Resources")
        print("-" * 63)

        print("[1] Anxiety")
        print("[2] Depression")
        print("[3] Stress")
        print("[4] PTSD (Post-Traumatic Stress Disorder)")
        print("[5] OCD (Obsessive-Compulsive Disorder)")
        print("[6] Bipolar Disorder")
        print("[7] Eating Disorders")
        print("[8] Phobias")
        print("[9] Panic disorder")
        print("[10] Antisocial personality disorder (ASPD)")
        print("[U] Useful resources to learn more")
        print("[X] Exit")

        user_input = input("> ").strip().lower()

        if user_input == "x":
            return

        if user_input in MENTAL_HEALTH_RESOURCES:
            selected_topic = MENTAL_HEALTH_RESOURCES[user_input]
            while True:
                clear_screen()
                print(PATIENT_BANNER_STRING)
                print(f"Learn More About: {selected_topic['name']}")
                print("-" * 55)

                # Display summary and resources
                print(f"Summary:\n{selected_topic['summary']}\n")
                print("Useful Resources:")
                for resource in selected_topic["resources"]:
                    print(f"- {resource}")

                print("\nWhat would you like to do next?")
                print("[R] Return to Learn More dashboard")
                print("[X] Exit")

                next_action = input("> ").strip().lower()

                if next_action == "r":
                    break  # Go back to the "Learn More" dashboard
                elif next_action == "x":
                    return
                else:
                    print_system_message("Invalid choice. Please select [R] or [X].")
        else:
            print_system_message("Invalid choice. Please select a valid topic or [X] to exit.")



