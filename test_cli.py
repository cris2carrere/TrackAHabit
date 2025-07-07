import questionary

#questionary.print("Welcome to Track A Habit App!")
choices = questionary.select("What would you like to do?", choices=["create", "edit", "delete", "view", "exit"]).ask()


print("You selected:", choices)