import gc
import os
from analytics import get_habit_analytics
from database import (
    get_db_connection,
    initialize_tables,
    get_predefined_habits,
    get_habits_by_period,
    close_db_connection
)
from datetime import datetime, timedelta
from habits import Habit


class TestTrackAHabit:

    def setup_method(self):
        if os.path.exists('test_habit.db'):
            os.remove('test_habit.db')
        self.db = get_db_connection('test_habit.db')
        initialize_tables(self.db)
        predefined_habits = get_predefined_habits(self.db)

        for habit in predefined_habits:
            periodicity_id_from_db = self.db.cursor().execute('''SELECT Name FROM Periodicity WHERE ID = ?''', (habit[3],)).fetchone()
            habit = Habit(habit[1], habit[2], periodicity_id_from_db[0])
            created_at = (datetime.now() - timedelta(weeks=5)).strftime("%Y-%m-%d %H:%M:%S")
            habit.add_habit(self.db, created_at)

        daily_habit = get_habits_by_period(self.db, "Daily")
        assert len(daily_habit) == 3, "There should be three daily habits."

    def test_daily_habit(self):
        daily_habit = get_habits_by_period(self.db, "Daily")
        assert len(daily_habit) == 3, "There should be three daily habits."

    def test_weekly_habit(self):
        weekly_habit = Habit("Learn a Language", "Practice language weekly", "Weekly")
        # Check off the habit for 4 consecutive weeks
        for i in range(4):
            checked_at = (datetime.now() - timedelta(weeks=i)).strftime("%Y-%m-%d %H:%M:%S")
            weekly_habit.checkoff_habit(self.db, checked_at)

        longest_streak, _ = get_habit_analytics(self.db, weekly_habit.name)
        assert longest_streak == 4, "Longest streak should be 4 weeks."

    def test_monthly_habit(self):
        monthly_habit = Habit("Read a Book", "Read a book per month", "Monthly")

        # Check off the habit for 2 consecutive months
        for i in range(2):
            checked_at = (datetime.now() - timedelta(days=i * 30)).strftime("%Y-%m-%d %H:%M:%S")
            monthly_habit.checkoff_habit(self.db, checked_at)

        longest_streak, _ = get_habit_analytics(self.db, monthly_habit.name)
        assert longest_streak == 2, "Longest streak should be 2 months."

    def teardown_method(self):
        close_db_connection(self.db)
        gc.collect()
        if os.path.exists('test_habit.db'):
            os.remove('test_habit.db')
