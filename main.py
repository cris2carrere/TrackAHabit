import questionary
from habits import Habit
from database import (
    get_db_connection,
    get_all_habits,
    check_habit,
    initialize_tables,
)
from analytics import (
    list_all_tracked_habits,
    list_habits_by_periodicity,
    longest_run_streak_habit,
)


def cli_ui():
    print("Welcome to Track A Habit App!")

    # Initialize the database connection and create predefined data
    db = get_db_connection()
    initialize_tables(db)

    user_options = [
        "Create Habit",
        "Check a Habit",
        "List Habits",
        "Analyze Habits",
        "Exit Application",
    ]

    periodicity_options = [
        "Daily",
        "Weekly",
        "Monthly"
    ]

    while True:
        choice = questionary.select("\nWhat would you like to do?",
                                    choices=user_options).ask()

        if choice == "Create Habit":
            name = questionary.text("\nEnter the habit name:").ask()

            description = questionary.confirm("\nWould you like to add a description?").ask()  # NOQA: E

            if description:
                description = questionary.text("\nEnter the habit description:").ask()  # NOQA: E

            else:
                description = ""

            periodicity = questionary.select("Select the periodicity:", choices=periodicity_options).ask()  # NOQA: E

            habit = Habit(name, description, periodicity)

            habit.add_habit(db)

        elif choice == "Check a Habit":
            habits = get_all_habits(db)

            if len(habits) == 0:
                print("There aren't any habits to check, please create one habit first")  # NOQA: E
                questionary.text("Press Enter to continue...").ask()

            else:
                habit_names = []

                for habit in habits:
                    habit_names.append(habit[1])

                selected_habit = questionary.select("Complete habit:", choices=habit_names).ask()  # NOQA: E

                check_habit(db, selected_habit)

        elif choice == "List Habits":
            list_choice = questionary.select("Please select an option", choices=["View All Habits", "View All Habits Same Period"]).ask()  # NOQA: E

            if list_choice == "View All Habits":
                habits = list_all_tracked_habits(db)

                print("\nList of every habit:\n")

                for habit in habits:
                    print(f"Name: # {habit[1]}")
                print("\n")

                questionary.text("Press Enter to continue...").ask()

            elif list_choice == "View All Habits Same Period":
                periodicity_choice = questionary.select("Select a periodicity:", choices=periodicity_options).ask()  # NOQA: E

                habits_by_period = list_habits_by_periodicity(db, periodicity_choice)  # NOQA: E

                print("\nList of every habit:\n")

                for habit in habits_by_period:
                    print(f"Name: # {habit[1]}")
                print("\n")

                questionary.text("Press Enter to continue...").ask()

        elif choice == "Analyze Habits":
            analyze_options = [
                "Longest Streak For All Habits",
                "Longest Run For A Habit",
                "Habit struggle analysis",
            ]

            analyze_choice = questionary.select("Select an analysis option:", choices=analyze_options).ask()  # NOQA: E

            if analyze_choice == "Longest Streak For All Habits":
                habits = get_all_habits(db)

                habits_longest_run = []

                for habit in habits:
                    longest_run, current_run = longest_run_streak_habit(db, habit[1])  # NOQA: E
                    habits_longest_run.append((habit[1], longest_run, current_run))  # NOQA: E
                    print(f"{habit[1]} longest run is: {longest_run}, current run is: {current_run}")  # NOQA: E

                questionary.text("Press Enter to continue...").ask()

            elif analyze_choice == "Longest Run For A Habit":
                habits = get_all_habits(db)

                if len(habits) == 0:
                    print("There aren't any habits to check, please create one habit first")  # NOQA: E
                    questionary.text("Press Enter to continue...").ask()
                else:
                    selected_habit = questionary.select("Select a habit:", choices=[habit[1] for habit in habits]).ask()  # NOQA: E
                    longest_streak, current_streak = longest_run_streak_habit(db, selected_habit)  # NOQA: E

                    print(f"{selected_habit} longest run streak is: {longest_streak} days, your current streak is: {current_streak}")  # NOQA: E

            elif analyze_choice == "Habit struggle analysis":
                pass

        elif choice == "Exit Application":
            print("Exiting the Track A Habit. Goodbye!")
            break


if __name__ == "__main__":
    cli_ui()
