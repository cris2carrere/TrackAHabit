import datetime
from database import (
    get_all_habits,
    get_habits_by_period,
    get_habit_creation_date,
    get_tracked_habit,
    get_habit_periodicity,
    get_db_connection,
)


def list_all_tracked_habits(db):
    """"
    List all tracked habits from the database.
    :param habits: List of all habits"""
    return get_all_habits(db)


def list_habits_by_periodicity(db, periodicity):
    """"
    List habits by periodicity from the database."""
    return get_habits_by_period(db, periodicity)


def longest_run_streak_habit(db, selected_habit):
    habit_records = get_tracked_habit(db, selected_habit)
    periodicity = get_habit_periodicity(db, selected_habit)

    # loop through the habit records to find the longest run streak
    longest_streak = 0
    current_streak = 0
    previous_date = get_habit_creation_date(db, selected_habit)

    for record in habit_records:
        checked_at = datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S').date()  # NOQA: E

        if periodicity == 1:
            condition = is_next_day(checked_at, previous_date)
        elif periodicity == 2:
            condition = is_next_week(checked_at, previous_date)
        else:
            condition = is_next_month(checked_at, previous_date)

        if condition is True:  # NOQA: E501
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1  # Reset current streak

        # Update the longest streak if current streak is greater
        if longest_streak < current_streak:
            longest_streak = current_streak

        previous_date = checked_at

    return longest_streak, current_streak


def is_next_day(checked_at, previous_date):
    if checked_at == previous_date + datetime.timedelta(days=1) or checked_at == previous_date:  # NOQA: E
        return True
    else:
        return False


def is_next_week(checked_at, previous_date):
    year1, week1, _ = previous_date.isocalendar()
    year2, week2, _ = checked_at.isocalendar()

    # Get the last ISO week of year1, Dec 28 always last week
    last_week1 = datetime.date(year1, 12, 28).isocalendar()[1]

    # Check if date2 is in the next ISO week after date1
    is_next_week = (
        (year1 == year2 and week2 == week1 + 1) or
        (year2 == year1 + 1 and week1 == last_week1 and week2 == 1)
    )
    return True if is_next_week else False


def is_next_month(checked_at, previous_date):
    year_delta = checked_at.year - previous_date.year
    month_delta = checked_at.month - previous_date.month

    return (year_delta == 0 and month_delta == 1) or (year_delta == 1 and previous_date.month == 12 and checked_at.month == 1)  # NOQA: E
