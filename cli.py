import questionary
from models import Habit
from db import DB_Habit_Connection
from analytics import list_all_tracked_habits, \
    list_habits_by_periodicity, \
    longest_run_streak_for_all_habits, \
    longest_run_streak_habit


class CML_UI:
    """"
    Command Line Interface (CLI) User Interface for the application.
    This class provides a simple text-based interface for user interaction."""

    def __init__(self):
        self.run()

    def run(self):
        print("Welcome to Track A Habit App!")

        # Initialize the database connection and create predefined data
        db = DB_Habit_Connection()
        db.initialize_predefined_data()
        db.insert_periodicity()

        while True:
            choice = questionary.select("What would you like to do?", choices=["Create Habit", "Check a Habit", "List Habits", "Analyze Habits", "Check a Habit", "Exit"]).ask()
            if choice == "Create Habit":
                name = questionary.text("Enter the habit name:").ask()
                periodicity = questionary.select("Select the periodicity:", choices=["Daily", "Weekly", "Monthly"]).ask()
                db.add_habit(name, periodicity)

            elif choice == "Check a Habit":
                habits = db.get_habit_data()
                habit_names = []
                for habit in habits:
                    habit_names.append(habit[1])
                selected_habit = questionary.select("Select a habit to edit:", choices=habit_names).ask()
                print(f"You selected: {selected_habit}")
                db.check_habit(selected_habit)

            elif choice == "List Habits":
                list_choice = questionary.select("Please select an option", choices=["View All Habits", "View All Habits Same Period"]).ask()
                habits = db.get_all_habits()

                if list_choice == "View All Habits":
                    list_all_tracked_habits(habits)

                elif list_choice == "View All Habits Same Period":
                    periodicity_choice = questionary.select("Select a periodicity:", choices=["Daily", "Weekly", "Monthly"]).ask()
                    list_habits_by_periodicity(db, periodicity_choice)

            elif choice == "Analyze Habits":
                analyze_choice = questionary.select("Select an analysis option:", choices=["Longest Streak For All Habits", "Longest Run A Habit"]).ask()
                if analyze_choice == "Longest Streak For All Habits":
                    average_streak = longest_run_streak_for_all_habits(db)
                    print(f"Average streak: {average_streak} days")
                elif analyze_choice == "Longest Run A Habit":
                    longest_streak = longest_run_streak_habit(db.get_habit_data())
                    print(f"Longest run streak: {longest_streak} days")

            elif choice == "Edit":
                # habit_to_change = questionary.select("Select a habit to edit:", choices=db.get_all_habits()).ask()
                habits = db.get_habit_data()

                habit_names = []
                for habit in habits:
                    # append habit names to a list named habit_names
                    habit_names.append(habit[1])

                selected_habit = questionary.select("Select a habit to edit:", choices=habit_names).ask()
                print(selected_habit)

            elif choice == "Exit":
                print("Exiting the Track A Habit. Goodbye!")
                break
