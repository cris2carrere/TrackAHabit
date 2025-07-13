from database import insert_habit


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.completed_days = []

    def add_habit(self, db):
        insert_habit(db, self.name, self.description, self.periodicity)

    def __str__(self):
        return f"Habit name: {self.name}, description: {self.description}, frequency: {self.periodicity})"  # NOQA: E501
