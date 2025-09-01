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
    get_predefined_habits,
    close_db_connection,
    initialize_tables
)
from habits import Habit


def cli_ui():
    """
    Command Line Interface for the Track A Habit application.
    """
    print("Welcome to Track A Habit App!")

    db = get_db_connection()
    initialize_tables(db)

    # Definition of user options to control the application flow
    user_options = [
        "Create Habit",
        "View Predefined Habits",
        "Check off a Habit",
        "List Habits",
        "Analyze Habits",
        "Exit Application"
    ]

    periodicity_options = [
        "Daily",
        "Weekly",
        "Monthly"
    ]

    analyze_options = [
        "Longest Streak For All Habits",
        "Longest Run For A Habit",
        "Habit Struggle Analysis"
    ]

    list_options = [
        "View All Habits",
        "View All Habits Same Period"
    ]

    while True:
        choice = questionary.select("\nWhat would you like to do?",
                                    choices=user_options).ask()

        if choice == "Create Habit":
            name = questionary.text("\nEnter the habit name:").ask()

            if name == "":
                print("Habit name cannot be empty. Please try again.")
                continue

            description = questionary.confirm(
                "\nWould you like to add a description?").ask()
            if description:
                description = questionary.text(
                    "\nEnter the habit description:").ask()
            else:
                description = ""

            periodicity = questionary.select(
                "Select the periodicity:", choices=periodicity_options).ask()

            habit = Habit(name, description, periodicity)
            habit_created = habit.add_habit(db)

            if habit_created:
                print(habit, "| Created successfully!")
            else:
                questionary.text("Press Enter to continue...", qmark="#").ask()

        elif choice == "View Predefined Habits":
            habits = get_predefined_habits(db)

            if len(habits) == 0:
                print("\nThere are no predefined habits to display.\n")
            else:
                print("\nList of predefined habits:\n")
                for habit in habits:
                    if habit[3] == 1:
                        period = "Daily"
                    elif habit[3] == 2:
                        period = "Weekly"
                    elif habit[3] == 3:
                        period = "Monthly"
                    print(f"-Habit Name: {habit[1]} | Description: {habit[2]} | Periodicity: {period}")  # NOQA: E501
                print("\n")

            questionary.text("Press Enter to continue...", qmark="#").ask()

        elif choice == "Check off a Habit":
            habits = get_all_habits(db)

            if len(habits) == 0:
                print("\nThere are no habits to check off.\n")
                questionary.text("Press Enter to continue...", qmark="#").ask()
                continue
            else:
                selected_habit = questionary.select("Select a habit:", choices=[habit[1] for habit in habits]).ask()  # NOQA: E501

                habit = Habit(selected_habit, "", "")
                habit.checkoff_habit(db)

        elif choice == "List Habits":
            list_choice = questionary.select(
                "Please select an option", choices=list_options).ask()

            if list_choice == "View All Habits":
                habits = list_all_tracked_habits(db)

                if len(habits) == 0:
                    print("\nThere are no habits to display.\n")
                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501
                else:
                    print("\nList of all habits:\n")
                    for habit in habits:
                        print(f"- {habit[1]}")
                    print("\n")

                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501

            elif list_choice == "View All Habits Same Period":
                periodicity_choice = questionary.select(
                    "Select a periodicity:", choices=periodicity_options).ask()

                # Based on the selected periodicity, list habits
                habits_by_period = list_habits_by_periodicity(db, periodicity_choice)  # NOQA: E501

                if len(habits_by_period) == 0:
                    print(f"\nThere are no habits with {periodicity_choice} periodicity.\n")  # NOQA: E501
                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E
                    continue
                else:
                    print(f"\nList every {periodicity_choice} habit:\n")

                    for habit in habits_by_period:
                        print(f"- {habit[1]}")
                    print("\n")

                questionary.text("Press Enter to continue...", qmark="#").ask()

        elif choice == "Analyze Habits":
            # Display options for analyzing habits
            analyze_choice = questionary.select(
                "Select an analysis option:", choices=analyze_options).ask()

            if analyze_choice == "Longest Streak For All Habits":
                habits = get_all_habits(db)

                if len(habits) == 0:
                    print("\nThere aren't any habits to analyze, please create one habit first\n")  # NOQA: E501
                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501
                    continue

                else:
                    for habit in habits:
                        longest_run, period = get_habit_analytics(db, habit[1])
                        print(f"{habit[1]} longest run is: {longest_run} consecutive {period}")  # NOQA: E

                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501

            elif analyze_choice == "Longest Run For A Habit":
                habits = get_all_habits(db)

                if len(habits) == 0:
                    print("\nThere aren't any habits to analyze, please create one habit first\n")  # NOQA: E501
                    questionary.text("Press Enter to continue...").ask()

                else:
                    selected_habit = questionary.select("Select a habit:", choices=[habit[1] for habit in habits]).ask()  # NOQA: E
                    longest_run, period = get_habit_analytics(db, selected_habit)  # NOQA: E
                    print(f"{selected_habit} longest run streak is {longest_run} consecutive {period}")  # NOQA: E

                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501

            elif analyze_choice == "Habit Struggle Analysis":
                habits = get_all_habits(db)

                if len(habits) == 0:
                    print("\nThere aren't any habits to analyze, please create one habit first\n")  # NOQA: E501
                    questionary.text("Press Enter to continue...", qmark="#").ask()  # NOQA: E501
                else:
                    for habit in habits:
                        total_break_habit, period = struggle_habit(db, habit[1])  # NOQA: E501
                        if total_break_habit == 0:
                            print(f"Congrats! {habit[1]} has no breaks in the period {period}.")  # NOQA: E
                        else:
                            print(f"Total breaks for {habit[1]}: {total_break_habit}, period {period}")  # NOQA: E

                    questionary.text("Press Enter to continue...", qmark="###").ask()  # NOQA: E

        elif choice == "Exit Application":
            close_db_connection(db)
            print("Exiting the Track A Habit. Goodbye!")
            break


if __name__ == "__main__":
    cli_ui()
