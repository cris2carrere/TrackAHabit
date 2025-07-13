from database import insert_habit


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.completed_days = []

    def add_habit(self, db):
        insert_habit(db, self.name, self.description, self.periodicity)

    def complete(self, day):
        if day not in self.completed_days:
            self.completed_days.append(day)

    def mark_completed(self, day):
        return day in self.completed_days

    def calculate_streak(self):
        if not self.completed_days:
            return 0
        streak = 1
        sorted_days = sorted(self.completed_days)
        for i in range(1, len(sorted_days)):
            if sorted_days[i] == sorted_days[i - 1] + 1:
                streak += 1
            else:
                break
        return streak

    def __str__(self):
        return f"Habit name: {self.name}, description: {self.description}, frequency: {self.periodicity})"  # NOQA: E501
