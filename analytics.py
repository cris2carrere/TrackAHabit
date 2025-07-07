from db import get_habit_data


def calculate_average_streak(habit_data):
    """
    Calculate the average streak of completed habits.
    
    :param habit_data: List of tuples containing habit data.
    :return: Average streak of completed habits.
    """
    total_streak = 0
    count = 0

    for habit in habit_data:
        completed_days = habit[4]  # Assuming completed_days is at index 4
        if completed_days:
            streak = len(completed_days.split(','))
            total_streak += streak
            count += 1

    return total_streak / count if count > 0 else 0