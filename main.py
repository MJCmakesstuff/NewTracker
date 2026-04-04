import json
import sys
import time
import trackerFunctions as tf
from pathlib import Path

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
        
        self.manager = ListManager()
        self.settings = SettingsManager()

        # Creates a "data" directory if it doesn't exist.
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Sets data files to vars
        self.manager.load()

        # Loads settings
        self.settings.load()

        # Fixes the settings file if any of the settings are invalid.
        print("Checking settings file...") # KEEP
        self.settings.fix()

        #return self

    def main(self):
        print("Welcome to NewTracker! Hope you enjoy!!")
        print()

        windows = {
            "1": ("List Manager", self.list_manager),
            "2": ("Settings Editor", self.settings_editor)
        }

        while True:
            print("\nMain Menu")
            for key, (name, function) in windows.items():
                print(f"[{key}] {name}")
            print()
            window_choice = input(f"Which item would you like? (type \"{QUIT}\" to quit): ")
            if window_choice == QUIT:
                print("Thank you so much for using NewTracker! Come again!!")
                return 0
            elif window_choice in windows:
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
            userInput = input(f"What setting do you want to change? (type \"{RESET}\" to reset to defaults, or \"{BACK}\" to go to back): ")
            if userInput == BACK:
                print("Switching to main menu...")
                print()
                break

            elif userInput == RESET:
                self.settings.reset()
                continue

            else:
                setting = tf.checkInput(userInput, LOWER_PARAM)
                if tf.errorHandler(setting) != ALL_CLEAR:
                    tf.errorMessage(tf.errorHandler(setting))
                    continue
            
            if type(setting) == int:
                    try:
                        keys = list(self.settings.data.keys())
                        setting -= 1
                        setting = keys[setting]
                    except:
                        tf.errorMessage(DOESNT_EXIST)
                        continue

            # What to change to?
            if setting in self.settings.data:
                newValue = input("What would you like to change " + str(setting) + " to? ")
                if tf.checkSetting(newValue, self.settings.schema[setting]["type"], self.settings.schema[setting]["rules"]):
                    if self.settings.schema[setting]["rules"] == ["boolean"]:
                        newValue = tf.convertToBool(newValue)
                        #print(newValue, type(newValue))
                    self.settings.data[setting] = newValue
                    self.settings.save()
                    print("Changed " + str(setting) + " to " + str(newValue) + ".")
                    print()

                else:
                    continue
                # HERE
            else:
                tf.errorMessage(DOESNT_EXIST)
                continue

class ListManager:
    def __init__(self):
        self.lists = {}
        #self.ids = []
        self.fileLocation = Path("data") / "tracks.json"
        #self.schema = {"list name": {"item name": "integer"}}

    def createList(self, app, name=None, data=None):
        if data == None:
            data = {}
        if name == None:
            name = str(input("What would you like to name the list? ")).title()
        self.lists[name] = TrackList(name, data)
        print(f"Created list {name}")
        print()
        self.save()

    def deleteList(self, app, name=None):
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

    def getList(self, name):
        return self.lists.get(name)
    
    def save(self):
        toSave = {}
        for key, value in self.lists.items():
            toSave[key] = value.data
        tf.saveData(toSave, self.fileLocation)

    def load(self):
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

    def print(self, IDbool):
        if IDbool:
            for index, name in enumerate(self.lists.keys()):
                print(f"[{index}] {name}")
        else:
            for name in self.lists.keys():
                print(f"{name}")

    def openList(self, app):
        while True:
            print("Here are the lists: ")
            options = {}
            for index, (key, value) in enumerate(self.lists.items(), start=1):
                options[str(index)] = key
                print(f"[{index}] {key}")
            print()
            choice = input("Which one would you like to open? ")
            if choice in options:
                toOpen = True
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

                userInput = input(f"What do you want to {app.settings.data['mode']} by {app.settings.data['multiplier']}? (type \"{BACK}\" to go back): ")
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
                if app.settings.data["mode"] == ADD:
                    if app.manager.lists[currentList].add(track, int(app.settings.data["multiplier"])) == False:
                        continue
                elif app.settings.data["mode"] == SUBTRACT:
                    if app.manager.lists[currentList].subtract(track, int(app.settings.data["multiplier"])) == False:
                        continue
                app.manager.save()
    
class TrackList:
    def __init__(self, name, data=None):
        if data == None:
            data = {}
        self.data = data
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

    def add(self, track, multiplier):
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

    def subtract(self, track, multiplier):
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
        self.schema ={
        "settingsPersist": {
            "type": "rules",
            "rules": [
                "boolean"
            ],
            "default": True
        },
        "mode": {
            "type": "set",
            "rules": [
                "add",
                "subtract"
            ],
            "default": "add"
        },
        "multiplier": {
            "type": "rules",
            "rules": [
                "integer",
                "positive"
            ],
            "default": 1
        }
    }
        self.data = {}
        self.fileLocation = Path("data") / "settings.json"

    def load(self):
        loaded_data = tf.loadData(self.fileLocation, {})
        self.data = {}
        for key, value in self.schema.items():
            if key in loaded_data:
                self.data[key] = loaded_data[key]
            else:
                self.data[key] = value["default"]
        if self.data["settingsPersist"] == False:
            print("Settings persistence is turned off. Resetting settings to defaults...")
            self.reset()
        self.save()

    def save(self):
        tf.saveData(self.data, self.fileLocation)

    def reset(self):
        tf.resetSettings(self.data, self.schema, self.fileLocation)
        self.save()
    
    def fix(self):
        tf.fixSettingsFile(self.data, self.schema, self.fileLocation)
        print()
        tf.printSettings(self.data, {"ids": False})

    def print(self):
        tf.printSettings(self.data)   

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