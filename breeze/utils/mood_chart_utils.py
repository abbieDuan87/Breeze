from datetime import datetime

def plot_mood_chart(mood_entries):
    """
    Plots a simple ASCII mood chart.

    Args:
        mood_entries (list): A list of dictionaries containing mood and datetime.
                             Example:
                             [
                                 {"mood": "Very Happy", "datetime": "2024-12-01 10:00:00"},
                                 {"mood": "Neutral", "datetime": "2024-12-02 14:00:00"},
                                 ...
                             ]
    """
    # Define mood levels for y-axis
    mood_levels = {
        "Very Sad": 1,
        "Sad": 2,
        "Neutral": 3,
        "Happy": 4,
        "Very Happy": 5,
    }

    # Convert mood entries to x (dates) and y (mood levels)
    dates = [datetime.strptime(entry["datetime"], "%Y-%m-%d %H:%M:%S").date() for entry in mood_entries]
    moods = [mood_levels[entry["mood"]] for entry in mood_entries]

    # Get unique dates in sorted order for x-axis
    unique_dates = sorted(set(dates))

    # Create the graph
    print("\nMood Chart (ASCII Representation)")
    print("-" * 50)

    # Print y-axis and mood points
    for level_name, level in sorted(mood_levels.items(), key=lambda x: -x[1]):
        row = f"{level_name:<10}|"
        for date in unique_dates:
            # Check if there is a mood entry matching the current level and date
            row += " * " if any(mood == level and date == d for d, mood in zip(dates, moods)) else "   "
        print(row)

    # Print x-axis
    print(" " * 11 + "-" * (len(unique_dates) * 3))
    print(" " * 11 + " ".join(date.strftime("%d") for date in unique_dates))