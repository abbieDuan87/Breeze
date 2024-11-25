from breeze.utils.cli_utils import (
    clear_screen,
    print_system_message,
    direct_to_dashboard,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def learn_mental_health():
    # Data
    MENTAL_HEALTH_RESOURCES = {
        "a": {
            "name": "Anxiety",
            "summary": "Anxiety is a feeling of unease, such as worry or fear, that can be mild or severe.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/anxiety/"]
        },
        "d": {
            "name": "Depression",
            "summary": "Depression is a low mood that lasts a long time and affects your daily life.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/clinical-depression/"]
        },
        "s": {
            "name": "Stress",
            "summary": "Stress is the body's reaction to feeling threatened or under pressure.",
            "resources": ["https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/"]
        },
        "p": {
            "name": "PTSD (Post-Traumatic Stress Disorder)",
            "summary": "PTSD is a mental health condition triggered by a terrifying event.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/post-traumatic-stress-disorder-ptsd/"]
        },
        "o": {
            "name": "OCD (Obsessive-Compulsive Disorder)",
            "summary": "OCD is a common mental health condition where a person has obsessive thoughts and compulsive behaviours.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/obsessive-compulsive-disorder-ocd/"]
        },
        "b": {
            "name": "Bipolar Disorder",
            "summary": "Bipolar disorder is characterised by extreme mood swings, including emotional highs and lows.",
            "resources": ["https://www.nhs.uk/mental-health/conditions/bipolar-disorder/"]
        },
        "e": {
            "name": "Eating Disorders",
            "summary": "Eating disorders involve unhealthy eating behaviours and can affect mental and physical health.",
            "resources": ["https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/eating-disorders/overview/"]
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

        print("[A] Anxiety")
        print("[D] Depression")
        print("[S] Stress")
        print("[P] PTSD (Post-Traumatic Stress Disorder)")
        print("[O] OCD (Obsessive-Compulsive Disorder)")
        print("[B] Bipolar Disorder")
        print("[E] Eating Disorders")
        print("[U] Useful resources to learn more")
        print("[R] Return to dashboard")

        user_input = input("> ").strip().lower()

        if user_input == "r":
            direct_to_dashboard()
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
                print("[M] Return to Learn More dashboard")
                print("[R] Return to dashboard")

                next_action = input("> ").strip().lower()

                if next_action == "m":
                    break  # Go back to the "Learn More" dashboard
                elif next_action == "r":
                    direct_to_dashboard()
                    return
                else:
                    print_system_message("Invalid choice. Please select [M] or [D].")
        else:
            print_system_message("Invalid choice. Please select a valid topic or [R] to return.")



