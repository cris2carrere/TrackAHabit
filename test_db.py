import sqlite3
import datetime


class TestDB:
    def setup_method(self):
        pass

    def test_db(self):
        pass

    def teardown_method(self):
        pass

conn = sqlite3.connect('main.db')
conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
c = conn.cursor()



c.execute('''CREATE TABLE IF NOT EXISTS Periodicity (
    PeriodicityID INTEGER PRIMARY KEY AUTOINCREMENT,
    Periodicity TEXT NOT NULL)''')
c.connection.commit()


c.execute('''CREATE TABLE IF NOT EXISTS Habit_Plan (
    HabitID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Periodicity INTEGER NOT NULL,
    Created_At datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Periodicity) REFERENCES Periodicity(PeriodicityID))''')
c.connection.commit()

priority_data = [
    (1, 'Daily'),
    (2, 'Weekly'),
    (3, 'Monthly')]

c.executemany("INSERT INTO Periodicity VALUES (?, ?)", priority_data)
# c.execute("INSERT INTO Periodicity VALUES (?, ?)", (2, 'Weekly'))
# c.execute("INSERT INTO Periodicity VALUES (?, ?)", (3, 'Monthly'))
# conn.commit()

# c.execute("INSERT INTO Habit_Plan VALUES (?, ?, ?, ?)", (4, 'Ir con la luli al super', 2, datetime.datetime.now()))
conn.commit()

conn.close()