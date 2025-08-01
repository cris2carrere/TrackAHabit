from database import get_db_connection

db = get_db_connection()
# db.execute('''INSERT INTO Habit_Plan (Name, PeriodicityID, Description, CreatedAt) VALUES (?, ?, ?, ?)''', ("Doctor", 3, "Go to Doctor", "2025-01-08 00:00:00"))  # NOQA: E501
db.execute('INSERT INTO Habit_Tracker (HabitID, CompletedAt) VALUES (?, ?)', (3, "2025-02-08 00:00:00"))  # NOQA: E501
db.commit()
db.close()
