import sqlite3
from datetime import datetime, timedelta


def get_db_connection(name='habits.db'):
    """
    Get database connection
    :param name: name of the database
    :return: db connection
    """
    db = sqlite3.connect(name)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize_tables(db):
    # Create Periodicity table
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Periodicity (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL)''')
    db.commit()

    # Create Habit_Plan table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Plan (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        Description TEXT,
        PeriodicityID INTEGER NOT NULL,
        CreatedAt datetime DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (PeriodicityID) REFERENCES Periodicity(ID))''')
    db.commit()

    # Create Habit_Tracker table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Tracker (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        HabitID INTEGER,
        CompletedAt datetime DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (HabitID) REFERENCES Habit_Plan(ID))''')
    db.commit()

    insert_periodicity(db)
    db.close()


def insert_periodicity(db):
    cursor = db.cursor()
    if cursor.execute('SELECT COUNT(*) FROM Periodicity').fetchone()[0] > 0:
        pass
    else:
        frequency = ['Daily', 'Weekly', 'Monthly']
        # List comprehension to create a list of tuples for each frequency
        frequency_data = [(f,) for f in frequency]
        cursor.executemany("INSERT INTO Periodicity (Name) VALUES (?)", frequency_data)  # NOQA: E501
        cursor.connection.commit()


def insert_habit(db, name, description, periodicity):
    """
    Add a new habit to the database.
    :param name: habit name
    :param periodicity: habit periodicity
    """
    # Fetch the periodicity ID from the database
    db = get_db_connection()
    periodicity_id_from_db = db.execute('''SELECT ID FROM Periodicity WHERE Name = ?''', (periodicity,)).fetchone()  # NOQA: E501

    created_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    try:
        db.execute('''INSERT INTO Habit_Plan (Name, PeriodicityID, Description, CreatedAt) VALUES (?, ?, ?, ?)''', (name, periodicity_id_from_db[0], description, created_at))  # NOQA: E501
        db.commit()
        print(f"Habit '{name}' added to the database with periodicity '{periodicity}'.")  # NOQA: E501
    except sqlite3.IntegrityError:
        print(f"Habit '{name}' already exists in the database. Please choose a different name.")  # NOQA: E501
    db.close()


def get_all_habits(db):
    """
    Retrieve all habits from the database.
    :return: List of all habits
    """
    db = get_db_connection()
    cursor = db.cursor()
    selected_habit = cursor.execute('SELECT * FROM Habit_Plan').fetchall()
    db.close()
    return selected_habit


def get_habits_by_period(db, periodicity):
    """
    Retrieve all habits from the database.
    :param periodicity: Periodicity of the habit
    :return: List of all habits by selected periodicity
    """
    db = get_db_connection()
    cursor = db.cursor()
    habits_by_period = cursor.execute('SELECT * FROM Habit_Plan WHERE PeriodicityID = (SELECT ID FROM Periodicity WHERE Name = ?)', (periodicity,)).fetchall()  # NOQA: E501
    db.close()
    return habits_by_period


def check_habit(db, habit_name):
    """
    Mark a habit as completed into the Habit_Tracker table
    :param habit_name: Name of the habit to check
    """
    # Fetch the habit ID from the Habit_Plan table
    db = get_db_connection()
    cursor = db.cursor()
    habit_id = cursor.execute('SELECT ID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501

    # Insert record into Habit_Tracker table
    cursor.execute('INSERT INTO Habit_Tracker (HabitID) VALUES (?)', (habit_id,))  # NOQA: E501
    db.commit()
    db.close()


def get_habit_creation_date(db, habit_name):
    """
    Get habit creation date
    :param db: Database connection
    :param habit_name: habit name
    :return: datetime of habit creation date
    """
    db = get_db_connection()
    cursor = db.cursor()
    created_at = cursor.execute('SELECT CreatedAt FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    creation_date = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').date()  # NOQA: E501
    return creation_date


def get_habit_periodicity(db, habit_name):
    """
    Get the periodicity of a habit.
    :param db: Database connection
    :param habit_name: Name of the habit to get periodicity for
    :return: Periodicity of the habit
    """
    db = get_db_connection()
    cursor = db.cursor()
    periodicity = cursor.execute('SELECT PeriodicityID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    db.close()
    return periodicity


def get_tracked_habit(db, habit_name):
    """
    Get a tracked habit by its ID.
    :param db: Database connection
    :param habit_id: ID of the habit to retrieve
    :return: Habit details
    """
    db = get_db_connection()
    cursor = db.cursor()
    habit_id = cursor.execute('SELECT ID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    get_habit = cursor.execute('SELECT * FROM Habit_Tracker WHERE HabitID = ? ORDER BY CompletedAt ASC', (habit_id,)).fetchall()  # NOQA: E501
    db.close()
    return get_habit
