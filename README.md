# TrackAHabit Back-End App

A command-line habit tracking application that helps you build and maintain healthy habits through consistent monitoring and analytics. Track your daily activities directly from the command line, review your progress with detailed analytics.

## What is it?

TrackAHabit is a Python-based habit tracking system that allows users to:

- **Create Custom Habits**: Define habits with different periodicities (Daily, Weekly, Monthly)
- **Track Progress**: Mark habits as completed and maintain a completion history
- **Analyze Performance**: View detailed analytics including longest streaks and struggle analysis
- **Persistent Storage**: All data is stored in a local SQLite database for long-term tracking

The application features an interactive command-line interface built with questionary, making it easy to navigate through different options and manage your habits effectively.

## Features

- ✅ **Habit Management**: Create and list habits.
- ✅ **Progress Tracking**: Check off completed habits with timestamp tracking
- ✅ **Analytics Dashboard**: 
  - Longest streak analysis for individual or all habits
  - Current streak monitoring
  - Habit struggle analysis (missed completions)
- ✅ **Flexible Scheduling**: Support for daily, weekly, and monthly habit frequencies
- ✅ **Data Persistence**: SQLite database ensures your progress is never lost
- ✅ **User-Friendly CLI**: Interactive menu system with questionary

## Installation

Follow the below steps to run the application on your terminal.

**1. Clone the Repository**

``` shell
git clone https://github.com/cris2carrere/TrackAHabit.git
cd track_a_habit
```

**2. Create a Virtual Environment**

For Windows
``` shell
python -m venv venv
.\venv\Scritp\activate
```

For MacOS
``` shell
python3 -m venv venv
source venv/bin/activate
```

**3. Install requirements**

``` shell
pip install -r requirements.txt
```

## Usage

Start main.py and follow the instructions on screen.

```shell
python main.py
```

## Tests

```shell
pytest .
````

