import questionary
from analytics import (
    list_all_tracked_habits,
    list_habits_by_periodicity,
    get_habit_analytics,
    struggle_habit
)
from database import (
    get_db_connection,
    get_all_habits,
    check_habit,
    initialize_tables
)
from habits import Habit


def cli_ui():
    print("Welcome to Track A Habit App!")

    # Initialize the database connection and create predefined data
    db = get_db_connection()
    initialize_tables(db)

    # Define user options
    user_options = [
        "Create Habit",
        "Check a Habit",
        "List Habits",
        "Analyze Habits",
        "Exit Application",
    ]

    # Define Periodicity options
    periodicity_options = [
        "Daily",
        "Weekly",
        "Monthly"
    ]

    # Define analyze options
    analyze_options = [
        "Longest Streak For All Habits",
        "Longest Run For A Habit",
        "Habit struggle analysis",
    ]

    while True:

        choice = questionary.select("\nWhat would you like to do?",
                                    choices=user_options).ask()

        if choice == "Create Habit":
            name = questionary.text("\nEnter the habit name:").ask()

            if name == "":
                print("Habit name cannot be empty. Please try again.")
                continue

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
                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

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
                    print(f"Habit: {habit[1]}")
                print("\n")

                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

            elif list_choice == "View All Habits Same Period":
                periodicity_choice = questionary.select("Select a periodicity:", choices=periodicity_options).ask()  # NOQA: E

                habits_by_period = list_habits_by_periodicity(db, periodicity_choice)  # NOQA: E

                print("\nList of every habit:\n")

                for habit in habits_by_period:
                    print(f"Habit: {habit[1]}")
                print("\n")

                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

        elif choice == "Analyze Habits":
            analyze_choice = questionary.select("Select an analysis option:", choices=analyze_options).ask()  # NOQA: E

            if analyze_choice == "Longest Streak For All Habits":
                habits = get_all_habits(db)

                for habit in habits:
                    longest_run, _, _, period = get_habit_analytics(db, habit[1])  # NOQA: E
                    print(f"{habit[1]} longest run is: {longest_run} consecutive {period}")  # NOQA: E

                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

            elif analyze_choice == "Longest Run For A Habit":
                habits = get_all_habits(db)

                if len(habits) == 0:
                    print("There aren't any habits to analyze, please create one habit first")  # NOQA: E
                    questionary.text("Press Enter to continue...").ask()

                else:
                    selected_habit = questionary.select("Select a habit:", choices=[habit[1] for habit in habits]).ask()  # NOQA: E
                    longest_run, _, _, periodicity = get_habit_analytics(db,selected_habit)  # NOQA: E
                    print(f"{selected_habit} longest run streak is {longest_run} consecutive {periodicity}")  # NOQA: E

                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

            elif analyze_choice == "Habit struggle analysis":
                habits = get_all_habits(db)

                for habit in habits:
                    total_break_habit, period = struggle_habit(db, habit[1])
                    print(f"Total breaks for {habit[1]}: {total_break_habit}, period {period}")  # NOQA: E

                questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

        elif choice == "Exit Application":
            print("Exiting the Track A Habit. Goodbye!")
            break


if __name__ == "__main__":
    cli_ui()
