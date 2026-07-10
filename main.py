import csv
import sys
import trackerFunctions as tf
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime, time

DEBUG = True

#Solution to magic strings
QUIT = "quit"
BACK = "back"
RESET = "reset"
LOWER_PARAM = "lower"
ALL_CLEAR = "all clear"
DOESNT_EXIST = "That doesn't exist yet."
ADD = "add"
SUBTRACT = "subtract"
STATTIMEHUMAN = "human"
STATTIMETIMESTAMP = "timestamp"
STATTIMERELATIVE = "relative"

class App:
    def __init__(self):
        i = 0
        while i < 10:
            print()
            i += 1

        print("Starting up...")
        
        self.exit_value = 1

        self.manager = ListManager()
        self.settings = SettingsManager()
        self.statistics = Statistics()
        self.goals = Goals()

        self.export_csv_location = Path("data") / "data.csv"

        # Creates a "data" directory if it doesn't exist.
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Sets data files to vars
        self.manager.load()

        # Loads settings
        self.settings.load()

    def main(self):
        print("\nWelcome to NewTracker! Hope you enjoy!!")
        print()

        windows = {
            "1": ("List Manager", self.list_manager),
            "2": ("Settings Editor", self.settings_editor),
            "3": ("Statistics", self.statistics_viewer),
            "4": ("Goals", self.goals_viewer),
            "5": ("Other Actions", self.other_actions)
        }

        while True:
            if self.exit_value == 0:
                print("Thank you so much for using NewTracker! Come again!!")
                return 0
            
            print("\nMain Menu")
            for key, (name, function) in windows.items():
                print(f"[{key}] {name}")
            print()
            window_choice = input(f"Which item would you like? ")
            if window_choice in windows:
                name, function = windows[window_choice]
                i = 0
                while i < 10:
                    print()
                    i += 1
                function()
            else:
                tf.errorMessage(DOESNT_EXIST)

    def list_manager(self):
        print()
        print("Welcome to the list manager!")
        while True:
            print()
            print("Here are the lists: ")
            self.manager.print(False)
            print()
            print("Here are the options: ")
            options = {
                "1": ("Open List", self.manager.openList),
                "2": ("Create List", self.manager.createList),
                "3": ("Delete List", self.manager.deleteList)
            }
            for key, (name, function) in options.items():
                print(f"[{key}] {name}")
            print()
            choice = input(f"What would you like to do? (type \"{BACK}\" to go to back): ")
            if choice == BACK:
                print("Switching to main menu...")
                print()
                break
            elif choice in options:
                name, function = options[choice]
                function(self)
            else:
                tf.errorMessage(DOESNT_EXIST)

    def settings_editor(self):
        while True:
            print()
            self.settings.print()
            userInput = input(f"What setting do you want to change? (type \"{BACK}\" to go to back): ")
            if userInput == BACK:
                print("Switching to main menu...")
                print()
                break

            #Next two blocks see which setting to change
            else:
                setting = tf.checkInput(userInput, LOWER_PARAM)
                if tf.errorHandler(setting) != ALL_CLEAR:
                    tf.errorMessage(tf.errorHandler(setting))
                    continue
            
            if type(setting) == int:
                    try:
                        keys = list(self.settings.data.model_dump().keys())
                        setting -= 1
                        setting = keys[setting]
                    except:
                        tf.errorMessage(DOESNT_EXIST)
                        continue

            # What to change to?
            if hasattr(self.settings.data, setting):
                newValue = input(f"What do you want to change {setting} to? ")

                # Converts newValue to the correct type for setting.
                currentType = type(getattr(self.settings.data, setting))
                if currentType == bool:
                    newValue = tf.convertToBool(newValue)
                    if newValue == "not bool":
                        tf.errorMessage("This must be a boolean (true/false).")
                        continue
                elif currentType == int:
                    try:
                        newValue = int(newValue)
                    except ValueError:
                        tf.errorMessage("This must be an integer.")
                        continue
                    
                # Tries to update settings with new value.
                try:
                    data_dict = self.settings.data.model_dump()
                    data_dict[setting] = newValue
                    updated_data = Settings(**data_dict)
                    self.settings.data = updated_data
                    self.settings.save()
                    print("Changed " + str(setting) + " to " + str(newValue) + ".")
                    print()
                
                except ValidationError as e:
                    messages = [error['msg'] for error in e.errors()]
                    tf.errorMessage(f"Invalid value: {', '.join(messages)}")

            else:
                tf.errorMessage(DOESNT_EXIST)
                continue

    def statistics_viewer(self):
        while True:
            print()
            print("Here are the options: ")
            options = {
                "1": ("View Statistics", self.statistics.view_stats),
                "2": ("Change Time Settings", self.statistics.change_time_settings)
            }
            for key, (name, function) in options.items():
                print(f"[{key}] {name}")
            print()
            choice = input(f"What would you like to do? (type \"{BACK}\" to go back): ")
            if choice == BACK:
                break
            elif choice in options:
                name, function = options[choice]
                function(self)
            else:
                tf.errorMessage(DOESNT_EXIST)
        return

    def goals_viewer(self):
        while True:
            print()
            print("Here are the options: ")
            options = {
                "1": ("View Goals", self.goals.view_goals),
                "2": ("Add Goal", self.goals.add_goal),
                "3": ("Delete Goal", self.goals.delete_goal)
            }
            for key, (name, function) in options.items():
                print(f"[{key}] {name}")
            print()
            choice = input(f"What would you like to do? (type \"{BACK}\" to go back): ")
            if choice == BACK:
                break
            elif choice in options:
                name, function = options[choice]
                function()
            else:
                tf.errorMessage(DOESNT_EXIST)
        return

    def other_actions(self):
        print()
        options = {
            "1": ("Reset Settings", self.settings.reset),
            "2": ("Quit Program", self.exit_program),
            "3": ("Export to CSV", self.export_csv),
            "4": ("Import from CSV", self.import_csv)
        }

        while True:
            if self.exit_value == 0:
                return
            
            print("\nOther Actions")
            for key, (name, function) in options.items():
                print(f"[{key}] {name}")
            print()
            window_choice = input(f"Which item would you like? (type \"{BACK}\" to go back): ")
            if window_choice == BACK:
                break
            elif window_choice in options:
                name, function = options[window_choice]
                i = 0
                while i < 10:
                    print()
                    i += 1
                function()
            else:
                tf.errorMessage(DOESNT_EXIST)

    def exit_program(self):
        self.exit_value = 0

    def export_csv(self):
        userInput = tf.convertToBool(input(f"Exporting to CSV will overwrite any existing CSV file. Are you sure? (y/n) "))
        if userInput == "not bool" or not userInput:
            return
        with open(self.export_csv_location, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["list_name", "item_name", "value"])
            for list_name, track_list in self.manager.lists.items():
                for item_name, value in track_list.data.items():
                    writer.writerow([list_name, item_name, value])
        print(f"Data exported to {self.export_csv_location}")

    def import_csv(self):
        userInput = tf.convertToBool(input(f"Importing from CSV will overwrite any existing data. Are you sure? (y/n) "))
        if userInput == "not bool" or not userInput:
            return
        data = {}
        try:
            with open(self.export_csv_location, mode='r', newline='') as csv_file:
                reader = csv.DictReader(csv_file) # Creates list of rows (dicts) with keys from header row
                for row in reader:
                    try:
                        list_name = row["list_name"]
                        item_name = row["item_name"]
                        value = int(row["value"])
                        if list_name not in data:
                            data[list_name] = {}
                        data[list_name][item_name] = value
                    except (ValueError, KeyError):
                        print(f"Invalid data found, skipping row...")
        except FileNotFoundError:
            print(f"No CSV file found at {self.export_csv_location}. Try exporting data to CSV first.")
            return
        self.manager.load(data)
        print(f"Data imported from {self.export_csv_location}")
            
class ListManager:
    def __init__(self):
        self.lists = {} # {list name: TrackList object}
        #self.ids = []
        self.fileLocation = Path("data") / "tracks.json"
        #self.schema = {"list name": {"item name": "integer"}}

    def createList(self, app, name: str = None, data: dict = None) -> None:
        if data == None:
            data = {}
        if name == None:
            name = str(input("What would you like to name the list? ")).title()
        if name in self.lists.keys():
            tf.errorMessage("A list with that name already exists.")
            return
        self.lists[name] = TrackList(name, data)
        print(f"Created list {name}")
        print()
        self.save()

    def deleteList(self, app, name: str = None) -> None:
        if name == None:
            while True:
                print("Here are the lists: ")
                options = {}
                for index, (key, value) in enumerate(self.lists.items(), start=1):
                    options[str(index)] = key
                    print(f"[{index}] {key}")
                
                print()
                choice = input(f"Which one would you like to delete? (type \"{BACK}\" to go back): ")
                if choice == BACK:
                    print()
                    return
                if choice in options:
                    toDelete = True
                    break
                else:
                    tf.errorMessage(DOESNT_EXIST)
                    toDelete = False
                    break
            if toDelete:
                userInput = tf.convertToBool(input(f"This action cannot be undone. Are you sure? (y/n) "))
                if userInput == "not bool" or not userInput:
                    pass
                else: del self.lists[options[choice]]
        self.save()

    def getList(self, name: str) -> TrackList:
        return self.lists.get(name)
    
    def save(self):
        toSave = {}
        for key, value in self.lists.items():
            toSave[key] = value.data
        tf.saveData(toSave, self.fileLocation)

    def load(self, listData=None): # listData -> {"list name": {"item name": int}}
        self.lists = {}
        if listData == None:
            listData = tf.loadData(self.fileLocation, {})
        print("Checking data...") ## Checks storage of lists
        while True:
            delKey = None
            for key, value in listData.items():
                #print(f"Checking {key}: {value}")
                #print()
                delKey = None
                if tf.ruleChecker(key, ["non-empty", "string", "titleCase"], {"verbose": False}) and isinstance(value, dict):
                    #print("Rules passed")
                    pass

                else:
                    print("Invalid data found. Removing...")
                    delKey = key
                    #print(delKey)
                    break

            if delKey is None:
                break

            else:
                del listData[delKey] 
        
        for key, value in listData.items():
            self.lists[key] = TrackList(str(key), value) #####
        self.save()

    def print(self, IDbool: bool) -> None:
        if IDbool:
            for index, name in enumerate(self.lists.keys()):
                print(f"[{index}] {name}")
        else:
            for name in self.lists.keys():
                print(f"{name}")

    def openList(self, app: App) -> None:
        while True:
            print("Here are the lists: ")
            options = {}
            for index, (key, value) in enumerate(self.lists.items(), start=1):
                options[str(index)] = key
                print(f"[{index}] {key}")
            print()
            choice = input(f"Which one would you like to open? (type \"{BACK}\" to go back): ")
            if choice in options:
                toOpen = True
                break
            elif choice == BACK:
                print()
                toOpen = False
                break
            else:
                toOpen = False
                tf.errorMessage(DOESNT_EXIST)
                break

        if toOpen:
            currentList = options[choice]
            while True:
                print()
                print("Here's what I'm tracking so far: ")
                app.manager.lists[currentList].print()

                userInput = input(f"What do you want to {app.settings.data.mode} by {app.settings.data.multiplier}? (type \"{BACK}\" to go back): ")
                if userInput == BACK:
                    print("Switching to list manager...")
                    print()
                    break
                else:
                    track = tf.checkInput(userInput)

                if tf.errorHandler(track) != ALL_CLEAR:
                    tf.errorMessage(tf.errorHandler(track))
                    continue
                
                # If input is integer, tries to pull the corresponding item from tracksIndexes and set it as track.
                # If failed, that trackIndex doesn't exist, so print error and skip to next iteration.
                if type(track) == int:
                    #print("Track is integer, trying to match it to the correct key...")
                    try:
                        track -= 1
                        keyList = list(app.manager.lists[currentList].data.keys())
                        track = keyList[track]
                    except:
                        tf.errorMessage(DOESNT_EXIST)
                        continue
                
                # Adds or subtracts the track depending on the mode. 
                if app.settings.data.mode == ADD:
                    if app.manager.lists[currentList].add(track, int(app.settings.data.multiplier)) == False:
                        continue
                elif app.settings.data.mode == SUBTRACT:
                    if app.manager.lists[currentList].subtract(track, int(app.settings.data.multiplier)) == False:
                        continue
                app.manager.save()
    
class TrackList:
    def __init__(self, name: str, data: dict = None):
        if data == None:
            data = {}
        self.data = data # {item name: integer}
        self.name = name
        self.validate()
    
    def load(self):
        self.data = tf.loadData(self.fileLocation, {})
    
    def save(self):
        tf.saveData(self.data, self.fileLocation)

    def validate(self): #### Heres the problem
        print("Checking list data...") # Checks lists themselves
        while True:
            delKey = None
            for key, value in self.data.items():
                #print(f"Checking {key}: {value}")
                #print(f"of types {type(key)} and {type(value)}")
                delKey = None
                if tf.ruleChecker(key, ["non-empty", "string", "titleCase"], {"verbose": False}) and tf.ruleChecker(value, ["non-empty", "integer", "positive", "strict-non-string"], {"convertToInt": False, "verbose": False}):
                    pass

                else:
                    print("Invalid data found in tracks.json. Removing invalid data...")
                    delKey = key
                    break

            if delKey is None:
                break

            else:
                del self.data[delKey]
    
    def print(self):
        if app.settings.data.showGoalProgress:
            for index, (key, value) in enumerate(self.data.items(), start=1):
                print(f"[{index}] {key}: {value}")
                if self.name in app.goals.data and key in app.goals.data[self.name]:
                    goals = app.goals.data[self.name][key]
                    goal_progress_list = app.goals.calculate_goal_progress(self.name, key, {"get_percentage": False})
                    goal_expected_progress_list = app.goals.calculate_on_track_values(self.name, key)
                    for goal, progress, expected_value in zip(goals, goal_progress_list, goal_expected_progress_list):
                        print(f"  - Goal of value {goal[2]}: {app.goals.construct_progress_bar(progress, expected_value=expected_value)}")
        else: 
            tf.printTracks(self.data)

    def add(self, track: str, multiplier: int) -> bool:
        if track in self.data:
            self.data[track] += multiplier
            print("Added " + str(multiplier) + " to " + str(track) + ". New value: " + str(self.data[track]))
            print()
            app.statistics.updateList(self.name, track, multiplier)
            toReturn = True
        else:
            self.data[track] = multiplier
            print("Created " + str(track) + " with value " + str(self.data[track]) + ".")
            print()
            app.statistics.updateList(self.name, track, multiplier)
            toReturn = True
        return toReturn

    def subtract(self, track: str, multiplier: int) -> bool:
        if track in self.data:
            original_value = self.data[track]
            self.data[track] -= multiplier
            if self.data[track] <= 0:
                del self.data[track]
                print("Removed " + str(track) + ".")
                print()
                app.statistics.updateList(self.name, track, -original_value)
                toReturn = True
            else:
                print("Subtracted " + str(multiplier) + " from " + str(track) + ". New value: " + str(self.data[track]))
                print()
                app.statistics.updateList(self.name, track, -multiplier)
                toReturn = True
        else:
            tf.errorMessage(DOESNT_EXIST)
            toReturn = False
        return toReturn

class SettingsManager:
    def __init__(self):
        self.data: Settings = Settings()
        self.fileLocation = Path("data") / "settings.json"

    def load(self):

        loaded_data = tf.loadData(self.fileLocation, {})
        try:
            self.data = Settings(**loaded_data)
        except Exception as e:
            print(f"Error loading settings: {e}")
            print("Resetting settings to defaults...")
            self.data = Settings()

        if self.data.settingsPersist == False:
            print("Settings persistence is turned off. Resetting settings to defaults...")
            self.data = Settings()
            
        self.save()

    def save(self):
        tf.saveData(self.data.model_dump(), self.fileLocation)

    def reset(self):
        self.data = Settings()
        self.save()
        print("Settings reset.")

    def print(self):
        tf.printSettings(self.data.model_dump())   

class Statistics:
    def __init__(self):
        self.fileLocation = Path("data") / "statistics.json"
        self.load()

    def load(self):
        self.data = tf.loadData(self.fileLocation, {})

    def save(self):
        tf.saveData(self.data, self.fileLocation)

    def updateList(self, listName: str, item: str, value: int):
        if listName not in self.data:
            self.data[listName] = {
                "container": [datetime.now().timestamp(), datetime.now().timestamp()],
                "contents": {}
                } 
            self.save()
        if listName in self.data:
            self.data[listName]["container"][1] = datetime.now().timestamp()
            if item in self.data[listName]["contents"]: # if this item is already in the list
                self.data[listName]["contents"][item].append([datetime.now().timestamp(), value]) # add new timestamp and value to the list of this item
            else: # if this item is not already in the list
                self.data[listName]["contents"][item] = [[datetime.now().timestamp(), value]] # create a new list for this item with the first timestamp and value
            self.save()

    def view_stats(self, app):
        while True:
            print()
            print("Here are the lists: ")
            options = {}
            for index, (key, value) in enumerate(self.data.items(), start=1):
                options[str(index)] = key
                print(f"[{index}] {key}")
            print()
            choice = input(f"Which list would you like to view statistics for? (type \"{BACK}\" to go back): ")
            if choice == BACK:
                return
            elif choice in options:
                print()
                if app.settings.data.statTimeWindow > 0:
                    earliest_timestamp = datetime.now().timestamp() - app.settings.data.statTimeWindow
                    list_name = options[choice]
                    print(f"Statistics for list: {list_name}")
                    if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                        print(f"Date first modified: {datetime.fromtimestamp(self.data[list_name]['container'][0])}")
                        print(f"Date last modified: {datetime.fromtimestamp(self.data[list_name]['container'][1])}")
                    elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                        print(f"Timestamp first modified: {self.data[list_name]['container'][0]}")
                        print(f"Timestamp last modified: {self.data[list_name]['container'][1]}")
                    elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                        print(f"Relative time first modified: {(datetime.now().timestamp() - self.data[list_name]['container'][0])/86400:.2f} days ago")
                        print(f"Relative time last modified: {(datetime.now().timestamp() - self.data[list_name]['container'][1])/86400:.2f} days ago")
                    print()
                    if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                        print(f"Showing modifications since {datetime.fromtimestamp(earliest_timestamp)}:")
                    elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                        print(f"Showing modifications since timestamp {earliest_timestamp}:")
                    elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                        print(f"Showing modifications in the past {(app.settings.data.statTimeWindow / 86400):.2f} days:")
                    print()
                    for item, modifications in self.data[list_name]["contents"].items():
                        print(f"Item: {item}")
                        running_total = 0
                        for modification in modifications:
                            timestamp, value = modification
                            if timestamp >= earliest_timestamp:
                                running_total += value
                                if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                                    print(f"  - Date: {datetime.fromtimestamp(timestamp)}, Change: {value}")
                                elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                                    print(f"  - Timestamp: {timestamp}, Change: {value}")
                                elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                                    print(f"  - Relative time: {(datetime.now().timestamp() - timestamp)/86400:.2f} days ago, Change: {value}")
                        print()
                        if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                            print(f"Total change for {item} since {datetime.fromtimestamp(earliest_timestamp)}: {running_total}")
                        elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                            print(f"Total change for {item} since timestamp {earliest_timestamp}: {running_total}")
                        elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                            print(f"Total change for {item} in the past {(app.settings.data.statTimeWindow / 86400):.2f} days: {running_total}")
                        print()
                    input("Press Enter to continue...")

                elif app.settings.data.statTimeWindow == 0:
                    list_name = options[choice]
                    print(f"Statistics for list: {list_name}")
                    if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                        print(f"Date first modified: {datetime.fromtimestamp(self.data[list_name]['container'][0])}")
                        print(f"Date last modified: {datetime.fromtimestamp(self.data[list_name]['container'][1])}")
                    elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                        print(f"Timestamp first modified: {self.data[list_name]['container'][0]}")
                        print(f"Timestamp last modified: {self.data[list_name]['container'][1]}")
                    elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                        print(f"Relative time first modified: {(datetime.now().timestamp() - self.data[list_name]['container'][0])/86400:.2f} days ago")
                        print(f"Relative time last modified: {(datetime.now().timestamp() - self.data[list_name]['container'][1])/86400:.2f} days ago")
                    print()
                    print("Showing all modifications")
                    print()
                    for item, modifications in self.data[list_name]["contents"].items():
                        print(f"Item: {item}")
                        running_total = 0
                        for modification in modifications:
                            timestamp, value = modification
                            running_total += value
                            if app.settings.data.statTimeDisplay == STATTIMEHUMAN:
                                print(f"  - Date: {datetime.fromtimestamp(timestamp)}, Change: {value}")
                            elif app.settings.data.statTimeDisplay == STATTIMETIMESTAMP:
                                print(f"  - Timestamp: {timestamp}, Change: {value}")
                            elif app.settings.data.statTimeDisplay == STATTIMERELATIVE:
                                print(f"  - Relative time: {(datetime.now().timestamp() - timestamp)/86400:.2f} days ago, Change: {value}")
                        print()
                        print(f"Total change for {item}: {running_total}")
                        print()
                    input("Press Enter to continue...")
                else:
                    tf.errorMessage("Invalid statTimeWindow setting. It must be a non-negative number.")
                    return
            else:
                tf.errorMessage(DOESNT_EXIST)
            
    def change_time_settings(self, app):
        while True:
            setting_choice = None
            print()
            options = {
                "1": "Change statTimeDisplay",
                "2": "Change statTimeWindow"
            }
            print("Here are the options: ")
            for key, value in options.items():
                print(f"[{key}] {value}")
            print()
            setting_choice = input(f"What would you like to change? (type \"{BACK}\" to go back): ")
            if setting_choice == BACK:
                return
            elif setting_choice in options:
                break_from_inner_loop = False
                while True:
                    if setting_choice == "1":
                        setting_choice = None
                        while True:
                            display_choice = None
                            print()
                            options = {
                                "1": STATTIMEHUMAN,
                                "2": STATTIMETIMESTAMP,
                                "3": STATTIMERELATIVE,
                                "4": "What do these mean?"
                            }
                            print()
                            print("Here are the options: ")
                            for key, value in options.items():
                                print(f"[{key}] {value}")
                            print()
                            display_choice = input(f"What would you like to change statTimeDisplay to? (type \"{BACK}\" to go back): ")
                            if display_choice == BACK:
                                display_choice = None
                                break_from_inner_loop = True
                                break
                            elif display_choice in options:
                                if display_choice in ["1", "2", "3"]:
                                    app.settings.data.statTimeDisplay = options[display_choice]
                                    app.settings.save()
                                    print(f"Changed statTimeDisplay to {options[display_choice]}.")
                                    break_from_inner_loop = True
                                    display_choice = None
                                    break
                                elif display_choice == "4":
                                    print()
                                    print("Here are the explanations for each option:")
                                    print(f"1. {STATTIMEHUMAN}: Displays timestamps in a human-readable format (e.g., YYYY-MM-DD HH:MM:SS).")
                                    print(f"2. {STATTIMETIMESTAMP}: Displays timestamps as Unix timestamps (seconds since epoch).")
                                    print(f"3. {STATTIMERELATIVE}: Displays timestamps as relative time (e.g., X days ago).")
                                    print()
                                    display_choice = None
                                    input("Press Enter to continue...")
                            else:
                                tf.errorMessage(DOESNT_EXIST)
                            
                    elif setting_choice == "2":
                        setting_choice = None
                        break_from_inner_inner_loop = False
                        while True:
                            unit_choice = None
                            print()
                            options = {
                                "1": ("seconds", 1),
                                "2": ("minutes", 60),
                                "3": ("hours", 3600),
                                "4": ("days", 86400),
                                "5": ("weeks", 604800),
                                "6": ("months (30 days)", 2592000),
                                "7": ("years (365 days)", 31536000),
                                "8": ("all-time", 0)
                            }
                            for key, (name, multiplier) in options.items():
                                print(f"[{key}] {name}")
                            print()
                            unit_choice = input(f"Which unit of time would you like to use for statTimeWindow? (type \"{BACK}\" to go back): ")
                            if unit_choice == BACK:
                                unit_choice = None
                                break_from_inner_loop = True
                                break
                            if unit_choice in options:
                                if unit_choice == "8":
                                    app.settings.data.statTimeWindow = 0
                                    app.settings.save()
                                    print()
                                    print(f"Changed statTimeWindow to {app.settings.data.statTimeWindow}.")
                                    unit_choice = None
                                    break_from_inner_loop = True
                                    break
                                else:
                                    unit_name, multiplier = options[unit_choice]
                                    break_from_inner_inner_loop = False
                                    while True:
                                        try:
                                            value = float(input(f"Enter the number of {unit_name} for statTimeWindow: "))
                                            if value < 0:
                                                print("Please enter a non-negative number.")
                                                continue
                                            app.settings.data.statTimeWindow = value * multiplier
                                            app.settings.save()
                                            print()
                                            print(f"Changed statTimeWindow to {app.settings.data.statTimeWindow}.")
                                            unit_choice = None
                                            break_from_inner_loop = True
                                            break_from_inner_inner_loop = True
                                            break
                                        except ValueError:
                                            print("Please enter a valid number.")
                                            unit_choice = None
                            else:
                                tf.errorMessage(DOESNT_EXIST)
                            if break_from_inner_inner_loop:
                                break   
                    
                    elif break_from_inner_loop:
                        break
            else:
                tf.errorMessage(DOESNT_EXIST)

class Goals:
    def __init__(self):
        self.fileLocation = Path("data") / "goals.json"
        self.load()

    def load(self):
        self.data = tf.loadData(self.fileLocation, {})

    def save(self):
        tf.saveData(self.data, self.fileLocation)

    def view_goals(self):
        for list_name, items in self.data.items():
            print()
            print(f"List: {list_name}")
            for item_name, goals in items.items():
                print()
                print(f"Item: {item_name}")
                goal_progress_list = app.goals.calculate_goal_progress(list_name, item_name, {"get_percentage": False})
                goal_expected_progress_list = app.goals.calculate_on_track_values(list_name, item_name)
                for goal, progress, expected_value in zip(goals, goal_progress_list, goal_expected_progress_list):
                    print()
                    start_time = datetime.fromtimestamp(goal[0])
                    if goal[1] is not None:
                        end_time = datetime.fromtimestamp(goal[1])
                    else:
                        end_time = "No end time"
                    goal_value = goal[2]
                    print(f"  - Goal value: {goal_value}, Start time: {start_time}, End time: {end_time}")
                    print(f"    {app.goals.construct_progress_bar(progress, expected_value=expected_value)}")
            print()
            tf.errorMessage()
        print()

    def add_goal(self):
        break_from_loop_1 = False
        while True: #Which list? (loop)
            if break_from_loop_1:
                break
            print()
            print("Here are the lists: ")
            options = {}
            for index, (key, value) in enumerate(app.manager.lists.items(), start=1):
                options[str(index)] = key
                print(f"[{index}] {key}")
            print()
            list_choice = input(f"Which list would you like to add a goal to? (type \"{BACK}\" to go back): ")
            if list_choice == BACK:
                break
            elif list_choice in options:
                break_from_loop_2 = False
                while True: #Which item? (loop 2)
                    if break_from_loop_2:
                        break
                    print()
                    print(f"Here are the items in {options[list_choice]}: ")
                    item_options = {}
                    for index, (key, value) in enumerate(app.manager.lists[options[list_choice]].data.items(), start=1):
                        item_options[str(index)] = key
                        print(f"[{index}] {key}")
                    print()
                    item_choice = input(f"Which item would you like to add a goal for? (type \"{BACK}\" to go back): ")
                    if item_choice == BACK:
                        break
                    elif item_choice in item_options:
                        break_from_loop_3 = False
                        while True: #Goal specs (loop 3)
                            if break_from_loop_3:
                                break
                            print()
                            goal_value = input(f"What is the goal value for {item_options[item_choice]}? (type \"{BACK}\" to go back): ")
                            if goal_value == BACK:
                                break
                            try:
                                goal_value = int(goal_value)
                                if goal_value <= 0:
                                    tf.errorMessage("Please enter a positive integer.")
                                    continue
                                else:
                                    break_from_loop_4 = False
                                    while True: #When does the goal end? (loop 4)
                                        if break_from_loop_4:
                                            break
                                        end_time_input = input(f"How many days from now does this goal end? (type \"{BACK}\" to go back, or \"0\" for no end date): ")
                                        if end_time_input == BACK:
                                            break_from_loop_4 = True
                                            break
                                        try:
                                            end_time_input = float(end_time_input)
                                            if end_time_input < 0:
                                                tf.errorMessage("Please enter a non-negative number.")
                                                continue
                                            else:
                                                if end_time_input == 0:
                                                    end_time = None
                                                else:
                                                    end_time = datetime.now().timestamp() + (end_time_input * 86400)
                                                if options[list_choice] not in self.data:
                                                    self.data[options[list_choice]] = {}
                                                if item_options[item_choice] not in self.data[options[list_choice]]:
                                                    self.data[options[list_choice]][item_options[item_choice]] = []
                                                self.data[options[list_choice]][item_options[item_choice]].append([datetime.now().timestamp(), end_time, goal_value])
                                                self.save()
                                                if end_time is None:
                                                    print(f"Added goal for {item_options[item_choice]} in {options[list_choice]}: {goal_value} with no end date.")
                                                else:
                                                    print(f"Added goal for {item_options[item_choice]} in {options[list_choice]}: {goal_value} before {datetime.fromtimestamp(end_time)}.")
                                                break_from_loop_1 = True
                                                break_from_loop_2 = True
                                                break_from_loop_3 = True
                                                break_from_loop_4 = True
                                                tf.errorMessage()
                                                break
                                        except ValueError:
                                            tf.errorMessage("Please enter a valid number.")
                                            continue

                            except Exception as e:
                                #print(e)
                                tf.errorMessage("Please enter a valid integer.")
                                continue
                    else:
                        tf.errorMessage(DOESNT_EXIST)
                        continue
            else:
                tf.errorMessage(DOESNT_EXIST)
                continue

    def delete_goal(self):
        break_from_loop_1 = False
        while True: #Which list? (loop)
            if break_from_loop_1:
                break
            print()
            print("Here are the lists with goals: ")
            list_options = {}
            for index, (key, value) in enumerate(self.data.items(), start=1):
                print(f"[{index}] {key}")
                list_options[str(index)] = key
            print()
            list_choice = input(f"Which list would you like to delete a goal from? (type \"{BACK}\" to go back): ")
            if list_choice == BACK:
                break
            elif list_choice in list_options:
                break_from_loop_2 = False
                while True: #Which item? (loop 2)
                    if break_from_loop_2:
                        break
                    print()
                    print(f"Here are the items with goals in {list_options[list_choice]}: ")
                    item_options = {}
                    for index, (key, value) in enumerate(self.data[list_options[list_choice]].items(), start=1):
                        print(f"[{index}] {key}")
                        item_options[str(index)] = key
                    print()
                    item_choice = input(f"Which item would you like to delete a goal from? (type \"{BACK}\" to go back): ")
                    if item_choice == BACK:
                        break
                    elif item_choice in item_options:
                        break_from_loop_3 = False
                        while True: #Which goal? (loop 3)
                            if break_from_loop_3:
                                break
                            print()
                            print(f"Here are the goals for {item_options[item_choice]} in {list_options[list_choice]}: ")
                            goal_options = {}
                            for index, goal in enumerate(self.data[list_options[list_choice]][item_options[item_choice]], start=1):
                                print(f"[{index}] Goal value: {goal[2]}")
                                goal_options[str(index)] = index - 1
                            print()
                            goal_choice = input(f"Which goal would you like to delete? (type \"{BACK}\" to go back): ")
                            if goal_choice == BACK:
                                break
                            elif goal_choice in goal_options:
                                del self.data[list_options[list_choice]][item_options[item_choice]][goal_options[goal_choice]]
                                if len(self.data[list_options[list_choice]][item_options[item_choice]]) == 0:
                                    del self.data[list_options[list_choice]][item_options[item_choice]]
                                if len(self.data[list_options[list_choice]]) == 0:
                                    del self.data[list_options[list_choice]]
                                self.save()
                                print(f"Deleted goal for {item_options[item_choice]} in {list_options[list_choice]}.")
                                break_from_loop_1 = True
                                break_from_loop_2 = True
                                tf.errorMessage()
                                break
                            else:
                                tf.errorMessage(DOESNT_EXIST)
                                continue
                    else:
                        tf.errorMessage(DOESNT_EXIST)
                        continue
            else:
                tf.errorMessage(DOESNT_EXIST)
                continue

    def calculate_goal_progress(self, list_name: str, item_name: str, params: dict = None):
        default_params = {
            "get_percentage": True,
        }
        if params is not None:
            default_params.update(params)
            params = default_params
        else:
            params = default_params
        return_list = []
        if list_name not in self.data or item_name not in self.data[list_name]:
            return return_list
        for goal in self.data[list_name][item_name]:
            start_search_time = goal[0]
            end_search_time = goal[1] if goal[1] is not None else datetime.now().timestamp()
            running_total = 0
            for modification in app.statistics.data[list_name]["contents"][item_name]:
                if start_search_time <= modification[0] <= end_search_time:
                    running_total += modification[1]
            if params["get_percentage"]:
                amount_complete = running_total / goal[2] if goal[2] > 0 else 0
            else:
                if running_total >= goal[2]:
                    running_total = goal[2]
                elif running_total < 0:
                    running_total = 0
                amount_complete = [running_total, goal[2]]
            return_list.append(amount_complete)
        return return_list
    
    def construct_progress_bar(self, progress: list | float, bar_length: int = 20, expected_value: int = None, goal_state: str = None) -> str:
        if isinstance(progress, float | int):
            if progress < 0:
                progress = 0
            elif progress > 1:
                progress = 1
            filled_length = int(bar_length * progress)
        else: ## list [running_total, goal_value]
            if progress[0] < 0:
                progress[0] = 0
            elif progress[0] > progress[1]:
                progress[0] = progress[1]
            filled_length = int(bar_length * (progress[0] / progress[1]) if progress[1] > 0 else 0)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        if isinstance(progress, float | int):
            return f"[{bar}] {100 * progress:.2f}%"
        else:
            if goal_state is None:
                end_bar = f"[{bar}] {progress[0]}/{progress[1]} ({100 * (progress[0] / progress[1]):.2f}%)."
                if expected_value is not None:
                    end_bar += f" Expected: {expected_value} ({100 * (expected_value / progress[1]):.2f}%)."
                return end_bar

    def calculate_on_track_values(self, list_name: str, item_name: str) -> int:
        on_track_values = []
        if list_name not in self.data or item_name not in self.data[list_name]:
            return on_track_values
        for goal in self.data[list_name][item_name]:
            if goal[1] is not None:
                total_timespan = goal[1] - goal[0]
                current_timespan = datetime.now().timestamp() - goal[0]
                if current_timespan > total_timespan:
                    expected_value = goal[2]
                else:
                    percent_time_passed = current_timespan / total_timespan if total_timespan > 0 else 1
                    expected_value = int(goal[2] * percent_time_passed)
            else:
                expected_value = None
            on_track_values.append(expected_value)
        return on_track_values
    
    

class Settings(BaseModel):
    settingsPersist: bool = Field(default = True)
    mode: str = Field(default = "add")
    multiplier: int = Field(default = 1, gt = 0)
    statTimeDisplay: str = Field(default = STATTIMEHUMAN)
    statTimeWindow: float = Field(default = 604800, ge = 0)
    showGoalProgress: bool = Field(default = True)

    @field_validator("mode")
    def validate_mode(cls, value):
        if value not in ["add", "subtract"]:
            raise ValueError("Mode must be either 'add' or 'subtract'.")
        return value
    
    @field_validator("statTimeDisplay")
    def validate_statTimeDisplay(cls, value):
        if value not in [STATTIMEHUMAN, STATTIMETIMESTAMP, STATTIMERELATIVE]:
            raise ValueError(f"statTimeDisplay must be either \"{STATTIMEHUMAN}\", \"{STATTIMETIMESTAMP}\", or \"{STATTIMERELATIVE}\".")
        return value

if __name__ == "__main__":
    if DEBUG:
        app = App()
        sys.exit(app.main())
    else:
        try:
            app = App()
            sys.exit(app.main())
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)

def leppard():
    lyrics = ["Love bites, love bleeds", "It's bringing me to my knees", "Love lives, love dies", "It's no surprise", "Love begs, love pleads", "It's what I need"]
    for lyric in lyrics:
        print(lyric)
    sys.exit(1)