from database import check_habit, get_all_habits, insert_habit


class Habit:
    def __init__(self, name, description, periodicity):
        """
        Initializes a new Habit instance.
        :param name: The name of the habit.
        :param description: A description of the habit.
        :param periodicity: The frequency of the habit.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity

    def add_habit(self, db, created_at=None):
        """
        Inserts a new habit into the database.
        If the habit already exists, it will not be added again.
        Returns:
            bool: True if the habit was added successfully, False otherwise.
        """
        return insert_habit(db, self.name, self.description, self.periodicity, created_at)  # NOQA: E501

    def checkoff_habit(self, db, checked_at=None):
        """
        Checks off a habit by updating its status in the database
        """
        check_habit(db, self.name, checked_at)
        print(f"Habit '{self.name}' has been checked off successfully!")  # NOQA: E501

    def list_all_habits(self):
        """
        Retrieves all habits from the database.
        Returns:
            list: A list of all habits.
        """
        return get_all_habits()

    def __str__(self):
        """
        Returns a string representation of the habit.
        """
        if self.description == "":
            return f"Habit name: {self.name} | Frequency: {self.periodicity}"  # NOQA: E501
        else:
            return f"Habit name: {self.name} | Description: {self.description} | Frequency: {self.periodicity}"  # NOQA: E501
