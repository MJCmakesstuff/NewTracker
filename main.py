import csv
import sys
import trackerFunctions as tf
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationError

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

        self.export_csv_location = Path("data") / "data.csv"

        # Creates a "data" directory if it doesn't exist.
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Sets data files to vars
        self.manager.load()

        # Loads settings
        self.settings.load()

    def main(self):
        print("Welcome to NewTracker! Hope you enjoy!!")
        print()

        windows = {
            "1": ("List Manager", self.list_manager),
            "2": ("Settings Editor", self.settings_editor),
            "3": ("Other Actions", self.other_actions)
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
        with open(self.export_csv_location, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["list_name", "item_name", "value"])
            for list_name, track_list in self.manager.lists.items():
                for item_name, value in track_list.data.items():
                    writer.writerow([list_name, item_name, value])
        print(f"Data exported to {self.export_csv_location}")

    def import_csv(self):
        data = {}
        try:
            with open(self.export_csv_location, mode='r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    list_name = row["list_name"]
                    item_name = row["item_name"]
                    value = int(row["value"])
                if list_name not in data:
                    data[list_name] = {}
                data[list_name][item_name] = value
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
                choice = input("Which one would you like to delete? ")
                if choice in options:
                    toDelete = True
                    break
                else:
                    tf.errorMessage(DOESNT_EXIST)
                    toDelete = False
                    break
            if toDelete:
                del self.lists[options[choice]]
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
        print("Checking data...")
        #print(listData)
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
            self.lists[key] = TrackList(str(key), value)
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

    def validate(self):
        print("Checking data...")
        while True:
            delKey = None
            for key, value in self.data.items():
                #print(f"Checking {key}: {value}")
                #print()
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
        tf.printTracks(self.data)

    def add(self, track: str, multiplier: int) -> bool:
        if track in self.data:
            self.data[track] += multiplier
            print("Added " + str(multiplier) + " to " + str(track) + ". New value: " + str(self.data[track]))
            print()
            toReturn = True
        else:
            self.data[track] = multiplier
            print("Created " + str(track) + " with value " + str(self.data[track]) + ".")
            print()
            toReturn = True
        return toReturn

    def subtract(self, track: str, multiplier: int) -> bool:
        if track in self.data:
            self.data[track] -= multiplier
            if self.data[track] <= 0:
                del self.data[track]
                print("Removed " + str(track) + ".")
                print()
                toReturn = True
            else:
                print("Subtracted " + str(multiplier) + " from " + str(track) + ". New value: " + str(self.data[track]))
                print()
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

class Settings(BaseModel):
    settingsPersist: bool = Field(default = True)
    mode: str = Field(default = "add")
    multiplier: int = Field(default = 1, gt = 0)

    @field_validator("mode")
    def validate_mode(cls, value):
        if value not in ["add", "subtract"]:
            raise ValueError("Mode must be either 'add' or 'subtract'.")
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