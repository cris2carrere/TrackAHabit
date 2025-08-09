import datetime
from calendar import monthrange
from database import (
    get_all_habits,
    get_habits_by_period,
    get_habit_creation_date,
    get_tracked_habit,
    get_habit_periodicity,
)


def list_all_tracked_habits(db):
    """"
    List all tracked habits from the database.
    :param db: Database connection object
    :return: List of all tracked habits."""
    return get_all_habits(db)


def list_habits_by_periodicity(db, periodicity):
    """
    List habits by periodicity from the database.
    :param db: Database connection object
    :param periodicity: The periodicity to filter habits by.
    :return: List of habits that match the periodicity.
    """
    return get_habits_by_period(db, periodicity)


def add_months(dt, months):
    """
    Add months to a date (handles end-of-month correctly).
    :param dt: The date to which months will be added.
    :param months: The number of months to add.
    :return: A new date with the specified number of months added.
    """

    year = dt.year + (dt.month + months - 1) // 12
    month = (dt.month + months - 1) % 12 + 1
    day = min(dt.day, monthrange(year, month)[1])
    return datetime.datetime(year, month, day).date()


def get_expected_dates(start, end, frequency):
    """
    Generate a list of expected dates based on the start date, end date, and
    frequency. i.e.: If frequency is 1, it generates list from start to end.
    :param start: The start date.
    :param end: The end date.
    :param frequency: The frequency of the habit
    :return: A list of expected dates.
    """
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


def get_habit_analytics(db, selected_habit):
    """
    Get habit analytics for the selected habit.
    :param db: Database connection object
    :param selected_habit: The name of the habit to analyze.
    :return: A tuple containing the longest streak, current streak,
             break habits count, and periodicity name.
    """
    habit_records = get_tracked_habit(db, selected_habit)
    periodicity = get_habit_periodicity(db, selected_habit)
    today = datetime.datetime.now().date()

    longest_streak = 0
    current_streak = 0
    break_habit = 0
    previous_date = get_habit_creation_date(db, selected_habit)
    start_date = previous_date

    # Check if habit has records
    # If habit has 0 record it means it was created but never checked-offs
    if len(habit_records) == 0:
        periodicity_name = get_periodicity_name(db, periodicity)
        return 0, periodicity_name  # NOQA: E501
    else:
        # Loop through the habit records to find the longest run streak
        while start_date <= today:
            for record in habit_records:
                # Convert the checked_at string to a date object
                checked_at = datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S').date()  # NOQA: E

                # Check if the checked_at date is in the next period based on
                # the habit periodicity
                condition = is_next_period(checked_at, previous_date, periodicity)  # NOQA: E501

                # If the checked_at date is the next period, increment the
                # current streak
                if condition is True:  # NOQA: E501
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    break_habit += 1
                    current_streak = 1  # Reset current streak

                # Update the longest streak if current streak is greater
                if longest_streak < current_streak:
                    longest_streak = current_streak

                # previous_date = previous_date + datetime.timedelta(days=1)
                previous_date = checked_at
                start_date = start_date + datetime.timedelta(days=1)

        periodicity_name = get_periodicity_name(periodicity)
        return longest_streak, periodicity_name


def get_periodicity_name(periodicity):
    """
    Get the name of the periodicity based on its ID.
    :param periodicity: The periodicity ID
    :return: The name of the periodicity.
    """
    if periodicity == 1:  # Daily
        return "Days"
    elif periodicity == 2:  # Weekly
        return "Weeks"
    elif periodicity == 3:  # Monthly
        return "Months"


def is_next_period(checked_at, previous_date, periodicity):
    """
    depending on the periodicity, check if the checked_at date is the next
    period after the previous_date.
    :param checked_at: The date when the habit was checked.
    :param previous_date: The date of the last habit check.
    :param periodicity: The periodicity of the habit
    :return: True if checked_at is the next period after previous_date,
             False otherwise.
    """
    if periodicity == 1:  # Daily
        return is_next_day(checked_at, previous_date)
    elif periodicity == 2:  # Weekly
        return is_next_week(checked_at, previous_date)
    else:  # Monthly
        return is_next_month(checked_at, previous_date)


def is_next_day(checked_at, previous_date):
    """
    Check if the checked_at date is the next day or the same day as
    previous_date.
    :param checked_at: The date when the habit was checked.
    :param previous_date: The date of the last habit check.
    :return: True if checked_at is the next day or the same day as
    previous_date, False otherwise.
    """
    if checked_at == previous_date + datetime.timedelta(days=1):
        return True
    else:
        return False


def is_next_week(checked_at, previous_date):
    """
    Check if the checked_at date is the next week after previous_date.
    :param checked_at: The date when the habit was checked.
    :param previous_date: The date of the last habit check.
    :return: True if checked_at is the next week, False otherwise.
    """
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
    """
    Check if the checked_at date is the next month after previous_date.
    :param checked_at: The date when the habit was checked.
    :param previous_date: The date of the last habit check.
    :return: True if checked_at is the next month, False otherwise.
    """
    year_delta = checked_at.year - previous_date.year
    month_delta = checked_at.month - previous_date.month
    return (year_delta == 0 and month_delta == 1) or (year_delta == 1 and previous_date.month == 12 and checked_at.month == 1)  # NOQA: E


def struggle_habit(db, habit_name):
    """
    Check how many times a habit was not completed in the expected period.
    :param db: Database connection object
    :param habit_name: Name of the habit to check
    :return: break_habits_counter and periodicity_name
    """

    cursor = db.cursor()
    today = datetime.datetime.now().date()
    creation_date = get_habit_creation_date(db, habit_name)
    frequency = get_habit_periodicity(db, habit_name)
    expected_dates = get_expected_dates(creation_date, today, frequency)
    habit_id = cursor.execute('SELECT ID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    cursor.execute(
        "SELECT CompletedAt FROM Habit_Tracker WHERE HabitID = ?",
        (habit_id,)
    )
    completions = set(
        datetime.datetime.fromisoformat(row[0]).date() for row in cursor.fetchall()  # NOQA: E501
    )
    break_habits_counter = 0

    for date in expected_dates:
        if date in completions:
            pass
        else:
            break_habits_counter += 1

    periodicity_name = get_periodicity_name(frequency)
    return break_habits_counter, periodicity_name
