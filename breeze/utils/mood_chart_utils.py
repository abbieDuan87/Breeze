from datetime import datetime


def plot_mood_chart(mood_entries):
    """
    Plots a simple ASCII mood chart with month and date on the x-axis.
    """
    mood_levels = {
        "Very Sad": 1,
        "Sad": 2,
        "Neutral": 3,
        "Happy": 4,
        "Very Happy": 5,
    }

    dates = [datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").date() 
             for entry in mood_entries
            ]
    moods = [mood_levels[entry["mood"]] for entry in mood_entries]
    unique_dates = sorted(set(dates))

    cell_width = 7  # Width of each date column
    print("\nMood Chart")
    print("-" * (len(unique_dates) * cell_width + 11))  # Adjust line length dynamically

    # Print y-axis and mood points
    for level_name, level in sorted(mood_levels.items(), key=lambda x: -x[1]):
        row = f"{level_name:<10}|"
        for date in unique_dates:
            # Center the * in the cell
            row += f"{' * ' if any(mood == level and date == d for d, mood in zip(dates, moods)) else '   ':^{cell_width}}"
        print(row)

    # Print x-axis
    print(
        " " * 11 + "-" * (len(unique_dates) * cell_width)
    )  # Adjust x-axis line length
    x_labels = " " * 11 + "".join(
        f"{date.strftime('%b %d'):<{cell_width}}" for date in unique_dates
    )
    print(x_labels)
