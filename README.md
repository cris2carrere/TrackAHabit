# TrackAHabit Back-End App

A command-line habit tracking application that helps you build and maintain healthy habits through consistent monitoring and analytics.

## What is it?

TrackAHabit is a Python-based habit tracking system that allows users to:

- **Create Custom Habits**: Define habits with different periodicities (Daily, Weekly, Monthly)
- **Track Progress**: Mark habits as completed and maintain a completion history
- **Analyze Performance**: View detailed analytics including longest streaks, current streaks, and struggle analysis
- **Persistent Storage**: All data is stored in a local SQLite database for long-term tracking

The application features an interactive command-line interface built with questionary, making it easy to navigate through different options and manage your habits effectively.

## Features

- ✅ **Habit Management**: Create, list, and organize habits by periodicity
- ✅ **Progress Tracking**: Check off completed habits with timestamp tracking
- ✅ **Analytics Dashboard**: 
  - Longest streak analysis for individual or all habits
  - Current streak monitoring
  - Habit struggle analysis (missed completions)
- ✅ **Flexible Scheduling**: Support for daily, weekly, and monthly habit frequencies
- ✅ **Data Persistence**: SQLite database ensures your progress is never lost
- ✅ **User-Friendly CLI**: Interactive menu system with questionary

## Installation

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

