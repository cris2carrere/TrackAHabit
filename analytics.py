from db import DB_Habit_Connection


def list_all_tracked_habits(habits):
    """"
    List all tracked habits from the database.
    :param habits: List of all habits"""
    for habit in habits:
        print(f"Name: {habit[1]}")


def list_habits_by_periodicity(db, periodicity):
    db.cursor.execute('SELECT * FROM Habit_Plan WHERE PeriodicityID = (SELECT PeriodicityID FROM Periodicity WHERE Periodicity_Name = ?)', (periodicity,))
    habits = db.cursor.fetchall()
    for habit in habits:
        print(f"Name: {habit[1]}")


def longest_run_streak_for_all_habits(db):
    habits = db.get_all_habits()
    print("Longest run streak for all habits:")
    # Loop through each habits and calculate the longest run for each habit
    def longest_run_streak(db, habit_name):
        



    for habit in habits:
        longest_streak = longest_run_streak(db, habit[1])
        print(f"Longest run streak for {habit[1]}: {longest_streak} days")


def longest_run_streak_habit(db):
    pass
