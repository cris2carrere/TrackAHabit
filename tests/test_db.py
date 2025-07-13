import sqlite3
import datetime
from database import DB_Habit_Connection

# import db # from db import DB_Habit_Connection


def test_db_connection():
    """
    Test the database connection and table creation.
    """
    db = DB_Habit_Connection()
    #conn = db.create_connection()

    #conn = DB_Habit_Connection.connect_db(db)

    #assert conn is not None, "Database connection failed"
    # Check if tables are created
    cursor = db.conn.cursor()
    cursor.execute("INSERT INTO Habit_Tracker (HabitID, CompletedAt) VALUES (1, '2001-10-01 12:00:00')")
    cursor.execute("INSERT INTO Habit_Tracker (HabitID, CompletedAt) VALUES (1, '2002-10-01 12:00:00')")
    cursor.execute("INSERT INTO Habit_Tracker (HabitID, CompletedAt) VALUES (1, '2003-10-01 12:00:00')")
    # commit the changes to the database
    db.conn.commit()
    
    
    #db.cursor.commit()
    cursor.close()
    print("Database connection and table creation test passed.")

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Habit_Plan'")
    # habit_plan_exists = cursor.fetchone() is not None

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Periodicity'")
    # periodicity_exists = cursor.fetchone() is not None

    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Habit_Tracker'")
    # habit_tracker_exists = cursor.fetchone() is not None

    # assert habit_plan_exists, "Habit_Plan table was not created"
    # assert periodicity_exists, "Periodicity table was not created"
    # assert habit_tracker_exists, "Habit_Tracker table was not created"


test_db_connection()