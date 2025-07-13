from database import get_db_connection
from datetime import datetime, timedelta

db = DB_Habit_Connection()
db.initialize_predefined_data()
db.insert_periodicity()
habits = db.get_all_habits()

print(habits)
for habit in habits:
    print(f"Name: {habit[1]}")

# List all habits from Habit_Plan table
db.cursor.execute('SELECT DISTINCT HabitID FROM Habit_Tracker')
habits = db.cursor.fetchall()
print(f"Total habits tracked: {len(habits)}")

for habit in habits:
    # print(f"Calculating longest run for habit: {habit[0]}")
    # Get the Name of the habit from Habit_Plan table
    db.cursor.execute('SELECT Name FROM Habit_Plan WHERE HabitID = ?', (habit[0],))
    habit_name = db.cursor.fetchone()[0]
    print(f"Habit Name: {habit_name}")
    print(f"Calculating longest run for habit: {habit_name}")
    from_select_created = db.cursor.execute('SELECT Created_At FROM Habit_Plan WHERE HabitID = ?', (habit[0],))
    habit_creation_date = db.cursor.fetchone()[0]
    # print(f"Habit: {habit} ## Created At: {db.cursor.fetchone()[0]}")

    print(f"Habit: {habit_name} ## Created At: {habit_creation_date}")
    # convert habit_creation_date to a datetime object in the format of YYYY-MM-DD
    splited_date = habit_creation_date.split(" ")[0]  # Extract only the date part
    habit_creation_date = datetime.strptime(splited_date, "%Y-%m-%d").date()

    print(f"Habit Creation Date: {habit_creation_date}")

    db.cursor.execute('SELECT Checked_At FROM Habit_Tracker WHERE HabitID = ?', (habit[0],))

    consecutive_streak = 0

    for row in db.cursor.fetchall():
        print("$$$$$$$$")
        # store in a variable named checked_at the date when the habit was checked in the format of YYYY-MM-DD       
        checked_at = row[0]
        date_only = checked_at.split(" ")[0]  # Extract only the date part
        date_format = datetime.strptime(date_only, "%Y-%m-%d").date()
        print(date_only)
        if habit_creation_date + timedelta(days=1) == date_format:
            print("se sumo un dia")
        else:
            print("menor")
        #     consecutive_streak += 1
        #     print(f"Checked At: {date_only}"

      #  if checked_at
     #       counter += 
    #    print(f"Checked At: {row[0]}")
    
    #dates = [row[0] for row in db.cursor.fetchall()]
    #dates.sort()    
