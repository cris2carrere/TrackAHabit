import sqlite3
import datetime
import os


class DB_Habit_Connection:
    """
    Database connection class for managing habits.
    This class handles the connection to the database and provides methods for CRUD operations.
    """
    def __init__(self, db_name='habits.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
        self.cursor = self.conn.cursor()
        self.db_exists = os.path.exists(self.db_name)

    def initialize_predefined_data(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Periodicity (
            PeriodicityID INTEGER PRIMARY KEY AUTOINCREMENT,
            Periodicity_Name TEXT NOT NULL)''')
        self.cursor.connection.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Plan (
            HabitID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            PeriodicityID INTEGER NOT NULL,
            Created_At datetime DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (PeriodicityID) REFERENCES Periodicity(PeriodicityID))''')
        self.cursor.connection.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Tracker (
            HabitID INTEGER,
            Checked_At datetime DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (HabitID) REFERENCES Habit_Plan(HabitID))''')
        self.cursor.connection.commit()

    def insert_periodicity(self):
        # check if the Periodicity table is empty
        self.cursor.execute('SELECT COUNT(*) FROM Periodicity')
        count = self.cursor.fetchone()[0]
        if count > 0:
            pass
        else:
            frequency = ['Daily', 'Weekly', 'Monthly']
            # Prepare data for insertion
            # Using a list comprehension to create a list of tuples for each frequency
            frequency_data = [(f,) for f in frequency]
            self.cursor.executemany("INSERT INTO Periodicity (Periodicity_Name) VALUES (?)", frequency_data)
            self.cursor.connection.commit()

    def connect_db(self):
        """Establish a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        return self.connection

    def create_table(self):
        """
        Create the habits table if it does not exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                frequency TEXT NOT NULL,
                completed_days TEXT
            )
        ''')
        self.connection.commit()

    def add_habit(self, name, periodicity):
        """
        Add a new habit to the database.
        :param name: Name of the habit
        :param periodicity: Periodicity of the habit (e.g., Daily, Weekly, Monthly)
        """

        self.cursor.execute('''SELECT PeriodicityID FROM Periodicity WHERE Periodicity_Name = ?''', (periodicity,))

        # Fetch the periodicity ID from the database
        periodicity_from_db = self.cursor.fetchone()

        created_at = datetime.datetime.today()
        # Execute the insert statement
        self.cursor.execute('''
            INSERT INTO Habit_Plan (Name, PeriodicityID, Created_At) VALUES (?, ?, ?)
        ''', (name, periodicity_from_db[0], created_at))
        self.conn.commit()


    def get_all_habits(self):
        """
        Retrieve all habits from the database.
        :return: List of all habits
        """
        self.cursor.execute('SELECT * FROM Habit_Plan')
        habits = self.cursor.fetchall()
        return habits

    def get_habits_by_period(self, periodicity):
        """
        Retrieve all habits from the database.
        :param periodicity: Periodicity of the habit (e.g., Daily, Weekly,
        :return: List of all habits by selected periodicity
        """
        self.cursor.execute('SELECT * FROM Habit_Plan WHERE PeriodicityID = (SELECT PeriodicityID FROM Periodicity WHERE Periodicity_Name = ?)', (periodicity,))
        habits = self.cursor.fetchall()
        return habits
        #for habit in habits:
            # Fetch the periodicity name for each habit
            # self.cursor.execute('SELECT Periodicity_Name FROM Periodicity WHERE PeriodicityID = ?', (habit[2],))
            # periodicity_name = self.cursor.fetchone()
            # if periodicity_name:
            #    print(f"Habit: {habit[1]}, Periodicity: {periodicity_name[0]}")

    def check_habit(self, habit_name):
        habit_data = self.cursor.execute('SELECT HabitID FROM Habit_Plan WHERE Name = ?', (habit_name,))
        # fetch only habit_id from the Habit_Plan table
        habit_id = habit_data.fetchone()[0]
        self.cursor.execute('INSERT INTO Habit_Tracker (HabitID) VALUES (?)', (habit_id,))
        self.conn.commit()

    def delete_habit(self, habit_id):
        """
        Delete a habit from the database by its ID.
        :param habit_id: ID of the habit to delete
        """
        self.cursor.execute('DELETE FROM Habit_Plan WHERE HabitID = ?', (habit_id,))
        self.conn.commit()

    

    def get_habit_data(self):
        """Retrieve all habits from the database."""
        self.cursor.execute('SELECT * FROM Habit_Plan')
        return self.cursor.fetchall()