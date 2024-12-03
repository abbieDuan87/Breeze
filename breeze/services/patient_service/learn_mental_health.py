import time
from breeze.utils.ansi_utils import colorise
from breeze.utils.cli_utils import (
    clear_screen,
    print_system_message,
)
from breeze.utils.constants import PATIENT_BANNER_STRING


def learn_mental_health():
    # Data
    MENTAL_HEALTH_RESOURCES = {
        "1": {
            "name": "Anxiety",
            "summary": "Anxiety is a feeling of stress, panic or fear that can affect your everyday life physically and psychologically. Most people feel anxious or scared sometimes, but if it's affecting"
            " your life there are things you can try that may help. Support is also available if you're finding it hard to cope with anxiety, fear or panic. Anxiety can cause many different symptoms."
            " It might affect how you feel physically, mentally and how you behave. It's not always easy to recognise when anxiety is the reason you're feeling or acting differently."
            "\n\nTypes of Anxiety: \n- Generalised Anxiety Disorder (GAD) \n- Social Anxiety \n- Health Anxiety"
            " \n\nSymptoms of Anxiety: \n- Physical: faster/irregular heartbeat, headaches, chest pains \n- Mental: feeling tense, being unable to relax, worrying about the past or future "
            "\n- Changes in behaviour: not being able to enjoy your leisure time, difficulty looking after yourself"
            "\n\nThings you can try to help with anxiety: \n- Try talking about your feelings to a friend, family member, health professional or counsellor."
            "\n- Use calming breathing exercises \n- Exercise: activities such as running, walking, swimming and yoga can help you relax",
            "resources": ["https://www.nhs.uk/mental-health/conditions/anxiety/"],
        },
        "2": {
            "name": "Depression",
            "summary": "Depression is a low mood that lasts a long time and affects your daily life. It is more than feeling unhappy or fed up for a few days. Depression can cause a variety of physical, emotional, and behavioural symptoms that affect your well-being and everyday life."
            "\n\nSymptoms of Depression: \n- Physical: changes in appetite or weight, tiredness, difficulty sleeping \n- Emotional: feeling sad, hopeless, or tearful, losing interest in activities you usually enjoy "
            "\n- Changes in behaviour: avoiding social situations, difficulty concentrating, withdrawing from family and friends"
            "\n\nThings you can try to help with depression: \n- Talk to someone you trust about how you’re feeling, such as a friend, family member, or health professional."
            "\n- Engage in physical activities like walking, running, or yoga to boost your mood."
            "\n- Establish a regular routine, even if it feels challenging, to help create structure in your day.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/clinical-depression/"
            ],
        },
        "3": {
            "name": "Stress",
            "summary": "Stress is the body's reaction to feeling threatened or under pressure. It is a normal response but can become overwhelming if left unmanaged. Prolonged stress can impact physical and mental health, affecting your overall well-being."
            "\n\nSymptoms of Stress: \n- Physical: headaches, muscle tension, chest pain, changes in sleep patterns \n- Emotional: feeling irritable, overwhelmed, anxious, or low "
            "\n- Behavioural: changes in eating habits, increased use of alcohol or smoking, withdrawing from activities or people"
            "\n\nThings you can try to help with stress: \n- Break tasks into smaller, manageable steps to avoid feeling overwhelmed."
            "\n- Practice mindfulness or relaxation techniques, such as deep breathing or meditation."
            "\n- Take time for hobbies or activities you enjoy to unwind and recharge.",
            "resources": [
                "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/"
            ],
        },
        "4": {
            "name": "PTSD (Post-Traumatic Stress Disorder)",
            "summary": "PTSD is a mental health condition triggered by experiencing or witnessing a traumatic event. It can cause distressing symptoms that affect everyday life and relationships if left untreated."
            "\n\nSymptoms of PTSD: \n- Physical: trouble sleeping, feeling easily startled or on edge \n- Emotional: intense fear, sadness, or anger, feeling detached from others "
            "\n- Behavioural: avoiding places, people, or activities that remind you of the trauma, reliving the event through flashbacks or nightmares"
            "\n\nThings you can try to help with PTSD: \n- Talk to a healthcare provider or mental health professional to explore therapy options, such as trauma-focused cognitive behavioural therapy (CBT)."
            "\n- Practice grounding techniques to stay connected to the present moment during flashbacks or anxiety."
            "\n- Seek support from friends, family, or support groups to share your experiences.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/post-traumatic-stress-disorder-ptsd/"
            ],
        },
        "5": {
            "name": "OCD (Obsessive-Compulsive Disorder)",
            "summary": "OCD is a condition where intrusive thoughts (obsessions) lead to repetitive behaviours (compulsions) to reduce distress. It can affect your daily routine, relationships, and overall well-being."
            "\n\nSymptoms of OCD: \n- Obsessions: unwanted and intrusive thoughts, fears, or urges \n- Compulsions: repetitive behaviours or rituals to alleviate distress, such as excessive cleaning, checking, or counting "
            "\n- Emotional: anxiety, shame, or frustration related to obsessive thoughts or compulsive behaviours"
            "\n\nThings you can try to help with OCD: \n- Seek therapy, such as cognitive behavioural therapy (CBT), to help challenge and manage obsessive thoughts and compulsive behaviours."
            "\n- Gradually reduce compulsive behaviours through exposure and response prevention (ERP) therapy."
            "\n- Talk to a GP about medication options if therapy alone is not enough.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/obsessive-compulsive-disorder-ocd/"
            ],
        },
        "6": {
            "name": "Bipolar Disorder",
            "summary": "Bipolar disorder is a mental health condition characterised by extreme mood swings, including emotional highs (mania) and lows (depression). These mood swings can affect sleep, energy levels, and decision-making, impacting daily life."
            "\n\nSymptoms of Bipolar Disorder: \n- Manic episodes: feeling euphoric, overconfident, having reduced need for sleep \n- Depressive episodes: feeling hopeless, tired, or losing interest in activities "
            "\n- Mixed episodes: experiencing symptoms of both mania and depression at the same time"
            "\n\nThings you can try to help with Bipolar Disorder: \n- Seek professional support, such as therapy or counselling, to help manage mood swings."
            "\n- Consider medication options, such as mood stabilisers, prescribed by a healthcare provider."
            "\n- Maintain a consistent routine to help stabilise your mood.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/bipolar-disorder/"
            ],
        },
        "7": {
            "name": "Eating Disorders",
            "summary": "Eating disorders involve unhealthy eating behaviours that affect physical and mental health. Common types include anorexia nervosa, bulimia nervosa, and binge eating disorder. These conditions can lead to serious health complications if untreated."
            "\n\nSymptoms of Eating Disorders: \n- Physical: weight changes, fatigue, digestive issues \n- Emotional: fear of gaining weight, obsession with food or body image "
            "\n- Behavioural: avoiding meals, excessive exercise, binge eating, purging"
            "\n\nThings you can try to help with Eating Disorders: \n- Speak with a GP or mental health professional about your eating habits and feelings."
            "\n- Join support groups or therapy to address the emotional and psychological aspects of the disorder."
            "\n- Work with a dietitian to establish a healthy eating routine.",
            "resources": [
                "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/eating-disorders/overview/"
            ],
        },
        "8": {
            "name": "Phobias",
            "summary": "A phobia is an intense and overwhelming fear of a specific object, situation, or activity. It can interfere with daily life if the fear leads to avoidance or distress in certain situations."
            "\n\nSymptoms of Phobias: \n- Physical: sweating, trembling, rapid heartbeat when exposed to the phobia \n- Emotional: intense fear or anxiety, feeling powerless to control the reaction "
            "\n- Behavioural: avoiding situations or places related to the phobia, difficulty functioning in certain contexts"
            "\n\nThings you can try to help with Phobias: \n- Consider therapy, such as cognitive behavioural therapy (CBT), to help confront and manage the fear."
            "\n- Gradual exposure to the source of the phobia under professional guidance can help reduce anxiety over time."
            "\n- Practice relaxation techniques, such as deep breathing, to manage symptoms during exposure.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/phobias/overview/"
            ],
        },
        "9": {
            "name": "Panic Disorder",
            "summary": "Panic disorder is a condition where you experience recurrent, unexpected panic attacks. These attacks are episodes of intense fear that can include physical and emotional symptoms."
            "\n\nSymptoms of Panic Disorder: \n- Physical: chest pain, shortness of breath, dizziness, rapid heartbeat \n- Emotional: overwhelming fear, feeling like you're losing control or having a heart attack "
            "\n- Behavioural: avoiding places or situations where you've had a panic attack before"
            "\n\nThings you can try to help with Panic Disorder: \n- Seek therapy, such as cognitive behavioural therapy (CBT), to learn coping strategies."
            "\n- Practice deep breathing or mindfulness exercises to help calm yourself during an attack."
            "\n- Talk to your GP about medication options if panic attacks occur frequently.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/panic-disorder/"
            ],
        },
        "10": {
            "name": "Antisocial Personality Disorder (ASPD)",
            "summary": "ASPD is a mental health condition where a person consistently disregards or violates the rights of others. It may involve patterns of deceit, impulsivity, or aggression."
            "\n\nSymptoms of ASPD: \n- Emotional: lack of empathy, disregard for others' feelings, difficulty maintaining relationships \n- Behavioural: manipulation, lying, breaking laws, impulsivity "
            "\n- Long-term effects: difficulty maintaining employment, legal problems, strained personal relationships"
            "\n\nThings you can try to help with ASPD: \n- Seek long-term therapy, such as counselling or psychotherapy, to develop healthier behaviours."
            "\n- Work with a healthcare provider to address any co-occurring conditions, such as depression or substance abuse."
            "\n- Establish clear goals for managing impulses and improving relationships.",
            "resources": [
                "https://www.nhs.uk/mental-health/conditions/antisocial-personality-disorder/"
            ],
        },
        "u": {
            "name": "Useful Resources",
            "summary": "General resources to support mental health and well-being. These resources cover a wide range of mental health topics and provide self-help tips and professional support contacts."
            "\n\nAdditional Information: \n- Access NHS-approved tools and guides to manage mental health \n- Explore mental health helplines for immediate support "
            "\n- Find self-help resources and tips for various conditions",
            "resources": [
                "https://www.nhs.uk/mental-health/",
                "https://www.nhs.uk/every-mind-matters/",
                "https://www.nhs.uk/mental-health/self-help/",
                "https://www.nhs.uk/conditions/stress-anxiety-depression/mental-health-helplines/",
            ],
        },
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
                    print(f"- {colorise(text=resource, color=63, underline=True)}")

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
                    time.sleep(1)
        else:
            print_system_message(
                "Invalid choice. Please select a valid topic or [X] to exit."
            )
            time.sleep(1)
