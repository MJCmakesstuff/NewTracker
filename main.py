import json
import sys
import time
import trackerFunctions as tf
from pathlib import Path

DEBUG = False

class ListManager:
    def __init__(self):
        self.lists = {}

    def createList(self, name):
        self.lists[name] = TrackList(name)

    def getList(self, name):
        return self.lists.get(name)

class TrackList:
    def __init__(self, name):
        self.data = {}
        self.ids = []
        self.fileLocation = Path("data") / "tracks.json"
        self.name = name
    
    def load(self, source):
        self.data = tf.loadData(source, {})
        self.generateIDS()
    
    def save(self, deposit):
        tf.saveData(self.data, deposit)
        self.generateIDS()

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
                self.save(Path("data") / "tracks.json")

    def generateIDS(self):
        self.ids = list(self.data.keys())
    
    def print(self):
        tf.printTracks(self.data, self.ids)

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
        self.generateIDS()
        self.save(self.fileLocation)
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
        self.generateIDS()
        self.save(self.fileLocation)
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
    manager.createList("my list")

    # Creates a "data" directory if it doesn't exist.
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Sets data files to vars
    tracks_file = data_dir / "tracks.json"
    settings_file = data_dir / "settings.json"

    # Loads tracks, tracksIndexes, and settings from JSON files.
    #tracks = tf.loadData(tracks_file, {})
    manager.lists["my list"].load(tracks_file)
    #tf.saveData(tracks, tracks_file)
    manager.lists["my list"].save(tracks_file)

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
    manager.lists["my list"].validate()

    return tracks_file, settings_file, settings, manager

def track_editor(manager, settings, tracks_file, settings_file):
    while True:
        print()
        print("Here's what I'm tracking so far: ")
        manager.lists["my list"].print()

        userInput = input("What do you want to " + str(settings["mode"]) + " by " + str(settings["multiplier"]) + "? (type \"settings\" to change settings) ")
        if userInput == "settings":
            print("Switching to settings window...")
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
            try:
                track = manager.lists["my list"].ids[track]
            except:
                tf.errorMessage("That doesn't exist yet.")
                continue
        
        # Adds or subtracts the track depending on the mode.
        if settings["mode"] == "add":
            if manager.lists["my list"].add(track, int(settings["multiplier"])) == False:
                continue
        elif settings["mode"] == "subtract":
            if manager.lists["my list"].subtract(track, int(settings["multiplier"])) == False:
                continue

        manager.lists["my list"].save(tracks_file)

def settings_editor(manager, settings, tracks_file, settings_file):
    while True:
        print()
        tf.printSettings(settings)
        userInput = input("What setting do you want to change? (type \"done\" to finish, \"reset\" to reset to defaults, or \"quit\" to exit the program) ")
        if userInput == "done":
            print("Switching to main window...")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            break

        elif userInput == "quit":
            print("Thank you for using my program! See you next time!!")
            return 0

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
                    setting = list(settings.keys())[setting]
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

    tracks_file, settings_file, settings, manager = initializeData()
    
    print("Welcome to NewTracker! Hope you enjoy!!")
    time.sleep(1)
    print()

    windows = {
        "1": ("Track Editor", track_editor),
        "2": ("Settings Editor", settings_editor)
    }

    while True:
        print("\nMain Menu")
        time.sleep(0.1)
        for key, (name, function) in windows.items():
            print(f"[{key}] {name}")
            time.sleep(0.1)
        window_choice = input("Please type your option (type \"quit\" to quit): ")
        if window_choice == "quit":
            return 0
        elif window_choice in windows:
            name, function = windows[window_choice]
        function(manager, settings, tracks_file, settings_file)

if __name__ == "__main__":
    if DEBUG:
        sys.exit(main())
    else:
        try:
            sys.exit(main())
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)


