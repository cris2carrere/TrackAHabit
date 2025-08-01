from database import insert_habit, get_all_habits
from datetime import datetime


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.checkoffs = []

    def add_habit(self, db):
        insert_habit(db, self.name, self.description, self.periodicity)

    def checkoff_habit(self):
        self.checkoffs.append(datetime.now())
        print("CHECKED OFF HABIT")

    def get_checkoffs(self):
        return self.checkoffs

    # create a function that returns the list of created habits
    def list_all_habits(self, db):
        return get_all_habits(db)

    def __str__(self):
        if self.description == "":
            return f"Habit name: {self.name} | Frequency: {self.periodicity} was created successfully!"  # NOQA: E501
        else:
            return f"Habit name: {self.name} | Description: {self.description} | Frequency: {self.periodicity} was created successfully!"  # NOQA: E501
