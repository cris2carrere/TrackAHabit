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


def add_months(dt, months):
    """Add months to a date (handles end-of-month correctly)."""
    from calendar import monthrange

    year = dt.year + (dt.month + months - 1) // 12
    month = (dt.month + months - 1) % 12 + 1
    day = min(dt.day, monthrange(year, month)[1])
    return datetime.datetime(year, month, day).date()


def get_expected_dates(start, end, frequency):
    dates = []

    if frequency == 1:
        step = datetime.timedelta(days=1)
        while start <= end:
            dates.append(start)
            start += step

    elif frequency == 2:
        step = datetime.timedelta(weeks=1)
        while start <= end:
            dates.append(start)
            start += step

    elif frequency == 3:
        current = start
        while current <= end:
            dates.append(current)
            current = add_months(current, 1)

    else:
        raise ValueError(f"Unsupported frequency: {frequency}")

    return dates


def track_habit_completions(db, habit_information):
    print("In habit tracker completions function", habit_information)  # NOQA: E501
    db = get_db_connection()
    cursor = db.cursor()
    today = datetime.datetime.now().date()
    # habits = get_tracked_habit(db, habit_name)
    print(f"Expected dates for habit '{habit_information[1]}':")
    creation_date = get_habit_creation_date(db, habit_information)
    frequency = get_habit_periodicity(db, habit_information)
    expected_dates = get_expected_dates(creation_date, today, frequency)
    print(expected_dates)

    cursor.execute(
        "SELECT CompletedAt FROM Habit_Tracker WHERE HabitID = ?",
        (habit_information[0],)
    )
    completions = set(
        datetime.datetime.fromisoformat(row[0]).date() for row in cursor.fetchall()  # NOQA: E501
    )

    if frequency == 1:
        frequency_name = "Daily"
    elif frequency == 2:
        frequency_name = "Weekly"
    elif frequency == 3:
        frequency_name = "Monthly"

    print(f"\nHabit: {habit_information[1]} ({frequency_name})")
    for date in expected_dates:
        status = "✅" if date in completions else "❌"
        print(f"{date}: {status}")

    db.close()


def get_habit_analytics(db, selected_habit):
    habit_records = get_tracked_habit(db, selected_habit)
    periodicity = get_habit_periodicity(db, selected_habit)
    today = datetime.datetime.now().date()

    # Loop through the habit records to find the longest run streak
    longest_streak = 0
    current_streak = 0
    break_habit = 0
    previous_date = get_habit_creation_date(db, selected_habit)
    if len(habit_records) == 0:
        return 0, 0, 0
    else:
        while previous_date <= today:
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
                    break_habit += 1
                    current_streak = 1  # Reset current streak

                # Update the longest streak if current streak is greater
                if longest_streak < current_streak:
                    longest_streak = current_streak

                previous_date = previous_date + datetime.timedelta(days=1)

        return longest_streak, current_streak, break_habit


def is_next_day(checked_at, previous_date):
    #if checked_at == previous_date + datetime.timedelta(days=1) or checked_at == previous_date:  # NOQA: E
    if checked_at == previous_date:
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
