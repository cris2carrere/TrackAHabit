import questionary
from models import Habit
from db import DB_Habit_Connection


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

        # Main loop for user interaction
        # choice = questionary.select("What would you like to do?", choices=["Create", "Edit", "Delete", "View", "Exit"]).ask()

        while True:

            choice = questionary.select("What would you like to do?", choices=["Create Task", "Edit", "Delete", "View", "Check a Habit", "Exit"]).ask()
            
            if choice == "Create Task":
                name = questionary.text("Enter the name of the habit:").ask()
                periodicity = questionary.select("Select the periodicity:", choices=["Daily", "Weekly", "Monthly"]).ask()
                # Assuming the periodicity is stored as an integer ID in the database
                db.add_habit(name, periodicity)

            elif choice == "Edit":
                # habit_to_change = questionary.select("Select a habit to edit:", choices=db.get_all_habits()).ask()
                habits = db.get_habit_data()

                habit_names = []
                for habit in habits:
                    # append habit names to a list named habit_names
                    habit_names.append(habit[1])

                selected_habit = questionary.select("Select a habit to edit:", choices=habit_names).ask()
                print(selected_habit)

            elif choice == "Check a Habit":
                habits = db.get_habit_data()
                habit_names = []
                for habit in habits:
                    # append habit names to a list named habit_names
                    habit_names.append(habit[1])
                selected_habit = questionary.select("Select a habit to edit:", choices=habit_names).ask()
                print(f"You selected: {selected_habit}")


                db.check_habit(selected_habit)

            
            elif choice == "Delete":
                pass
            elif choice == "View":
                habits = db.get_all_habits()
                print("Your Habits:")
                for habit in habits:
                    print(f"ID: {habit[0]}, Name: {habit[1]}, Periodicity: {habit[2]}")
            elif choice == "Exit":
                print("Exiting the Track A Habit. Goodbye!")
                break



        #db.add_habit("cleana the house", 1, "2023-10-02 12:00:00")
        # habit_name = input("Enter the name of the habit: ")
        # habit_description = input("Enter a description for the habit: ")
        # habit_frequency = input("Enter the frequency of the habit (daily, weekly, monthly")
        # db.add_habit("clean", "clean the house", "daily")
        # print(f"You entered: {command}")
