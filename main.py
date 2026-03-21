import json
import sys
import time
import trackerFunctions as tf
from pathlib import Path

DEBUG = True

class ListManager:
    def __init__(self):
        self.lists = {}
        #self.ids = []
        self.fileLocation = Path("data") / "tracks.json"
        #self.schema = {"list name": {"item name": "integer"}}

    def createList(self, settings, name=None, data=None):
        if data == None:
            data = {}
        if name == None:
            name = str(input("What would you like to name the list? ")).title()
        self.lists[name] = TrackList(name, data)
        print(f"Created list {name}")
        time.sleep(0.1)
        print()
        self.save()

    def deleteList(self, settings, name=None):
        if name == None:
            while True:
                print("Here are the lists: ")
                time.sleep(0.1)
                options = {}
                for index, (key, value) in enumerate(self.lists.items(), start=1):
                    options[str(index)] = key
                    print(f"[{index}] {key}")
                    time.sleep(0.1)
                
                print()
                choice = input("Which one would you like to delete? ")
                if choice in options:
                    toDelete = True
                    break
                else:
                    tf.errorMessage("That doesn't exist yet.")
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
        for key, value in listData.items():
            self.lists[key] = TrackList(str(key), value)

    def print(self, IDbool):
        if IDbool:
            for index, name in enumerate(self.lists.keys()):
                print(f"[{index}] {name}")
                time.sleep(0.1)
        else:
            for name in self.lists.keys():
                print(f"{name}")
                time.sleep(0.1)

    def openList(self, settings):
        while True:
            print("Here are the lists: ")
            time.sleep(0.1)
            options = {}
            for index, (key, value) in enumerate(self.lists.items(), start=1):
                options[str(index)] = key
                print(f"[{index}] {key}")
                time.sleep(0.1)
            print()
            choice = input("Which one would you like to open? ")
            if choice in options:
                toOpen = True
                break
            else:
                toOpen = False
                tf.errorMessage("That doesn't exist yet.")
                break

        if toOpen: 
            track_editor(self, settings, options[choice])
        
class TrackList:
    def __init__(self, name, data=None):
        if data == None:
            data = {}
        self.data = data
        self.fileLocation = Path("data") / "oldTracks.json"
        self.name = name
    
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
                self.save()
    
    def print(self):
        tf.printTracks(self.data)

    def add(self, track, multiplier):
        if track in self.data:
            self.data[track] += multiplier
            print("Added " + str(multiplier) + " to " + str(track) + ". New value: " + str(self.data[track]))
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            toReturn = True
        else:
            self.data[track] = multiplier
            print("Created " + str(track) + " with value " + str(self.data[track]) + ".")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            toReturn = True
        return toReturn

    def subtract(self, track, multiplier):
        if track in self.data:
            self.data[track] -= multiplier
            if self.data[track] <= 0:
                del self.data[track]
                print("Removed " + str(track) + ".")
                time.sleep(0.5)
                print()
                time.sleep(0.1)
                toReturn = True
            else:
                print("Subtracted " + str(multiplier) + " from " + str(track) + ". New value: " + str(self.data[track]))
                time.sleep(0.5)
                print()
                time.sleep(0.1)
                toReturn = True
        else:
            tf.errorMessage("That doesn't exist yet.")
            toReturn = False
        return toReturn

SETTINGSSCHEMA = {
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

def initializeData():
    
    manager = ListManager()

    # Creates a "data" directory if it doesn't exist.
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Sets data files to vars
    manager.load()
    settings_file = data_dir / "settings.json"

    # Loads settings
    loaded_settings = tf.loadData(settings_file, {})
    settings = {}
    for key, value in SETTINGSSCHEMA.items():
        if key in loaded_settings:
            settings[key] = loaded_settings[key]
        else:
            settings[key] = value["default"]

    tf.saveData(settings, settings_file)

    if settings["settingsPersist"] == False:
        print("Settings persistence is turned off. Resetting settings to defaults...")
        tf.resetSettings(settings, SETTINGSSCHEMA, settings_file)
        tf.saveData(settings, settings_file)
    

    # Fixes the settings file if any of the settings are invalid.
    print("Checking settings file...")
    tf.fixSettingsFile(settings, SETTINGSSCHEMA, settings_file)
    print()
    tf.printSettings(settings, {"ids": False})

    # Checks to make sure the data is valid.
    #manager.lists["My List"].validate()

    return settings_file, settings, manager

def list_manager(manager, settings, settings_file):
    print()
    print("Welcome to the list manager!")
    while True:
        print()
        print("Here are the lists: ")
        time.sleep(0.1)
        manager.print(False)
        print()
        print("Here are the options: ")
        time.sleep(0.1)
        options = {
            "1": ("Open List", manager.openList),
            "2": ("Create List", manager.createList),
            "3": ("Delete List", manager.deleteList)
        }
        for key, (name, function) in options.items():
            print(f"[{key}] {name}")
            time.sleep(0.1)
        print()
        choice = input("What would you like to do? (type \"back\" to go to back): ")
        if choice == "back":
            print("Switching to main menu...")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            break
        elif choice in options:
            name, function = options[choice]
            function(settings)

def track_editor(manager, settings, currentList="My List"):
    while True:
        print()
        print("Here's what I'm tracking so far: ")
        manager.lists[currentList].print()

        userInput = input("What do you want to " + str(settings["mode"]) + " by " + str(settings["multiplier"]) + "? (type \"back\" to go back): ")
        if userInput == "back":
            print("Switching to list manager...")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            break
        else:
            track = tf.checkInput(userInput)

        if tf.errorHandler(track) != "all clear":
            tf.errorMessage(tf.errorHandler(track))
            continue
        
        # If input is integer, tries to pull the corresponding item from tracksIndexes and set it as track.
        # If failed, that trackIndex doesn't exist, so print error and skip to next iteration.
        if type(track) == int:
            print("Track is integer, trying to match it to the correct key...")
            try:
                track -= 1
                keyList = list(manager.lists[currentList].data.keys())
                track = keyList[track]
            except:
                tf.errorMessage("That doesn't exist yet.")
                continue
        
        # Adds or subtracts the track depending on the mode.
        if settings["mode"] == "add":
            if manager.lists[currentList].add(track, int(settings["multiplier"])) == False:
                continue
        elif settings["mode"] == "subtract":
            if manager.lists[currentList].subtract(track, int(settings["multiplier"])) == False:
                continue
        manager.save()

def settings_editor(manager, settings, settings_file):
    while True:
        print()
        tf.printSettings(settings)
        userInput = input("What setting do you want to change? (type \"reset\" to reset to defaults, or \"back\" to go to back): ")
        if userInput == "back":
            print("Switching to main menu...")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            break

        elif userInput == "reset":
            tf.resetSettings(settings, SETTINGSSCHEMA, settings_file)
            continue

        else:
            setting = tf.checkInput(userInput, "lower")
            if tf.errorHandler(setting) != "all clear":
                tf.errorMessage(tf.errorHandler(setting))
                continue
        
        if type(setting) == int:
                try:
                    keys = list(settings.keys())
                    setting -= 1
                    setting = keys[setting]
                except:
                    tf.errorMessage("That doesn't exist yet.")
                    continue

        # What to change to?
        if setting in settings:
            newValue = input("What would you like to change " + str(setting) + " to? ")
            if tf.checkSetting(newValue, SETTINGSSCHEMA[setting]["type"], SETTINGSSCHEMA[setting]["rules"]):
                if SETTINGSSCHEMA[setting]["rules"] == ["boolean"]:
                    newValue = tf.convertToBool(newValue)
                    #print(newValue, type(newValue))
                settings[setting] = newValue
                tf.saveData(settings, settings_file)
                print("Changed " + str(setting) + " to " + str(newValue) + ".")
                time.sleep(0.5)
                print()
                time.sleep(0.1)

            else:
                continue
            # HERE
        else:
            tf.errorMessage("That doesn't exist yet.")
            continue

def main():
    i = 0
    while i < 10:
        print()
        i += 1

    print("Starting up...")

    settings_file, settings, manager = initializeData()

    print("Welcome to NewTracker! Hope you enjoy!!")
    time.sleep(1)
    print()

    windows = {
        "1": ("List Manager", list_manager),
        "2": ("Settings Editor", settings_editor)
    }

    while True:
        print("\nMain Menu")
        time.sleep(0.1)
        for key, (name, function) in windows.items():
            print(f"[{key}] {name}")
            time.sleep(0.1)
        print()
        window_choice = input("Which item would you like? (type \"quit\" to quit): ")
        if window_choice == "quit":
            print("Thank you so much for using NewTracker! Come again!!")
            time.sleep(1)
            return 0
        elif window_choice in windows:
            name, function = windows[window_choice]
            i = 0
            while i < 10:
                print()
                i += 1
                time.sleep(0.05)
            function(manager, settings, settings_file)
        else:
            tf.errorMessage("That doesn't exist yet.")

if __name__ == "__main__":
    if DEBUG:
        sys.exit(main())
    else:
        try:
            sys.exit(main())
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)

def leppard():
    print("I don't wanna touch you too much, baby")