import sqlite3
from datetime import datetime, timedelta


def get_db_connection(name='habits.db'):
    """
    Get database connection
    :param name: name of the database
    :return: db connection
    """
    db = sqlite3.connect(name)
    # Enable foreign key support
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize_tables(db):
    """
    Initialize the database tables if they do not exist.
    :param db: Database connection
    """
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

    cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Default (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        Description TEXT,
        PeriodicityID INTEGER NOT NULL,
        CreatedAt datetime DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (PeriodicityID) REFERENCES Periodicity(ID))''')
    db.commit()

    insert_periodicity(db)
    insert_predefined_habits(db)


def insert_periodicity(db):
    """
    Insert predefined periodicity values into the Periodicity Table if not
    already present.
    :param db: Database connection
    """
    curs = db.cursor()

    if curs.execute('SELECT COUNT(*) FROM Periodicity').fetchone()[0] > 0:
        pass
    else:
        frequency = ['Daily', 'Weekly', 'Monthly']
        # List comprehension to create a list of tuples for each frequency
        frequency_data = [(f,) for f in frequency]
        curs.executemany("INSERT INTO Periodicity (Name) VALUES (?)", frequency_data)  # NOQA: E501
        curs.connection.commit()


def insert_predefined_habits(db):
    """
    Insert predefined habits into the Habit_Plan table if not already present.
    :param db: Database connection
    """
    cursor = db.cursor()

    if cursor.execute('SELECT COUNT(*) FROM Habit_Default').fetchone()[0] > 0:
        pass
    else:
        habits = [["Drink Water", "Drink Water daily", "Daily"],
                  ["Read a Book", "Read a book per month", "Monthly"],
                  ["Exercise", "Exercise for 30 minutes daily", "Daily"],
                  ["Healthy Eating", "Eat a balanced diet daily", "Daily"],
                  ["Learn a Language", "Practice language weekly", "Weekly"]]  # NOQA: E501

        # Define created_at as 4 weeks ago
        created_at = (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d %H:%M:%S")
        for habit in habits:
            cursor.execute('''INSERT INTO Habit_Default (Name, Description, PeriodicityID, CreatedAt) VALUES (?, ?, (SELECT ID FROM Periodicity WHERE Name = ?), ?)''', (habit[0], habit[1], habit[2], created_at))  # NOQA: E501
            db.commit()


def insert_habit(db, name, description, periodicity, created_at):
    """
    Add a new habit to the database.
    :param db: Database connection
    :param name: habit name
    :param description: habit description
    :param periodicity: habit periodicity
    :param created_at: Optional timestamp for when the habit was created
    """
    curs = db.cursor()

    periodicity_id_from_db = curs.execute('''SELECT ID FROM Periodicity WHERE Name = ?''', (periodicity,)).fetchone()  # NOQA: E501

    if created_at is None:
        created_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    try:
        curs.execute('''INSERT INTO Habit_Plan (Name, PeriodicityID, Description, CreatedAt) VALUES (?, ?, ?, ?)''', (name, periodicity_id_from_db[0], description, created_at))  # NOQA: E501
        db.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Habit '{name}' already exists in the database. Please choose a different name.")  # NOQA: E501
        return False


def get_all_habits(db):
    """
    Retrieve all habits from the database.
    :return: List of all habits
    """
    cursor = db.cursor()

    selected_habit = cursor.execute('SELECT * FROM Habit_Plan').fetchall()  # NOQA: E501
    return selected_habit


def get_predefined_habits(db):
    """
    Retrieve all predefined habits from the database.
    :param db: Database connection object
    :return: List of predefined habits
    """
    cursor = db.cursor()

    selected_habit = cursor.execute('SELECT * FROM Habit_Default').fetchall()  # NOQA: E501
    return selected_habit


def update_periodicity(db, habit_name, new_periodicity):
    """
    Update the periodicity of a habit.
    :param db: Database connection object
    :param habit_name: Name of the habit to update
    :param new_periodicity: New periodicity to set for the habit
    """
    cursor = db.cursor()
    cursor.execute('UPDATE Habit_Plan SET PeriodicityID = (SELECT ID FROM Periodicity WHERE Name = ?) WHERE Name = ?', (new_periodicity, habit_name))  # NOQA: E501
    db.commit()


def get_habits_by_period(db, periodicity):
    """
    Retrieve all habits from the database.
    :param db: Database connection object
    :param periodicity: Periodicity of the habit
    :return: List of all habits by selected periodicity
    """
    cursor = db.cursor()

    habits_by_period = cursor.execute('SELECT * FROM Habit_Plan WHERE PeriodicityID = (SELECT ID FROM Periodicity WHERE Name = ?)', (periodicity,)).fetchall()  # NOQA: E501
    return habits_by_period


def check_habit(db, habit_name, checked_at):
    """
    Mark a habit as completed into the Habit_Tracker table
    :param db: Database connection object
    :param habit_name: Name of the habit to check
    :param checked_at: Optional timestamp for when the habit was checked off
    """
    # Fetch the habit ID from the Habit_Plan table
    cursor = db.cursor()
    habit_id = cursor.execute('SELECT ID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501

    if checked_at is None:
        checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO Habit_Tracker (HabitID) VALUES (?)', (habit_id,))  # NOQA: E501
    else:
        # Insert record into Habit_Tracker table
        cursor.execute('INSERT INTO Habit_Tracker (HabitID, CompletedAt) VALUES (?, ?)', (habit_id, checked_at))  # NOQA: E501
    db.commit()


def get_habit_creation_date(db, habit_name):
    """
    Get habit creation date
    :param db: Database connection object
    :param habit_name: habit name
    :return: datetime of habit creation date
    """
    cursor = db.cursor()

    created_at = cursor.execute('SELECT CreatedAt FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    creation_date = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S').date()  # NOQA: E501
    return creation_date


def get_habit_periodicity(db, habit_name):
    """
    Get the periodicity of a habit.
    :param habit_name: Name of the habit to get periodicity for
    :return: Periodicity of the habit
    """
    cursor = db.cursor()

    periodicity = cursor.execute('SELECT PeriodicityID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    return periodicity


def get_tracked_habit(db, habit_name):
    """
    Get a tracked habit by its ID.
    :param db: Database connection object
    :param habit_name: Name of the habit to retrieve
    :return: Habit details
    """
    cursor = db.cursor()

    habit_id = cursor.execute('SELECT ID FROM Habit_Plan WHERE Name = ?', (habit_name,)).fetchone()[0]  # NOQA: E501
    get_habit = cursor.execute('SELECT * FROM Habit_Tracker WHERE HabitID = ? ORDER BY CompletedAt ASC', (habit_id,)).fetchall()  # NOQA: E501
    return get_habit


def close_db_connection(db):
    """
    Close the database connection.
    :param db: Database connection to close
    """
    db.close()
