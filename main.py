import json
import sys
import time
import trackerFunctions as tf
from pathlib import Path

DEBUG = True

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
    # Creates a "data" directory if it doesn't exist.
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Sets data files to vars
    tracks_file = data_dir / "tracks.json"
    settings_file = data_dir / "settings.json"

    # Loads tracks, tracksIndexes, and settings from JSON files.
    tracks = tf.loadData(tracks_file, {})

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

    # Saves the data (to prevent problems reading bad files)
    tf.saveData(tracks, tracks_file)

    # Fixes the settings file if any of the settings are invalid.
    print("Checking settings file...")
    tf.fixSettingsFile(settings, SETTINGSSCHEMA, settings_file)
    print()
    tf.printSettings(settings, {"ids": False})

    # Checks to make sure the data is valid.
    print("Checking data...")
    while True:
        delKey = None
        for key, value in tracks.items():
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
            del tracks[delKey]
            tf.saveData(tracks, tracks_file)

    tracksIndexes = list(tracks.keys())

    return data_dir, tracks_file, settings_file, tracks, settings, tracksIndexes

def main():
    #int("freaky") # Traceback
    i = 0
    while i < 5:
        print()
        i += 1

    print("Starting up...")

    data_dir, tracks_file, settings_file, tracks, settings, tracksIndexes = initializeData()
    
    print("Welcome to NewTracker! Hope you enjoy!!")

    # Loop of Death
    while True:
        if settings["mode"] == "add" or settings["mode"] == "subtract":
            while True:
                print()
                print("Here's what I'm tracking so far: ")
                tf.printTracks(tracks, tracksIndexes)

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
                        track = tracksIndexes[track]
                    except:
                        tf.errorMessage("That doesn't exist yet.")
                        continue
                
                # If the track exists, add 1.
                # Otherwise, create the track, and add it to the index list.
                if track in tracks:
                    if settings["mode"] == "add":
                        tracks[track] += int(settings["multiplier"])
                        print("Added " + str(settings["multiplier"]) + " to " + str(track) + ". New value: " + str(tracks[track]))
                        time.sleep(0.5)
                        print()
                        time.sleep(0.1)

                    elif settings["mode"] == "subtract":
                        tracks[track] -= int(settings["multiplier"])
                        if tracks[track] <= 0:
                            del tracks[track]
                            tracksIndexes.remove(track)
                            print("Removed " + str(track) + ".")
                            time.sleep(0.5)
                            print()
                            time.sleep(0.1)
                        
                        else:
                            print("Subtracted " + str(settings["multiplier"]) + " from " + str(track) + ". New value: " + str(tracks[track]))
                            time.sleep(0.5)
                            print()
                            time.sleep(0.1)

                else:
                    if settings["mode"] == "add":
                        tracks[track] = int(settings["multiplier"])
                        tracksIndexes.append(track)
                        print("Created " + str(track) + " with value " + str(tracks[track]) + ".")
                        time.sleep(0.5)
                        print()
                        time.sleep(0.1)

                    elif settings["mode"] == "subtract":
                        tf.errorMessage("That doesn't exist yet.")
                        continue

                # Saves the data back to the JSON files.
                tf.saveData(tracks, tracks_file)



        else:
            tf.errorMessage("That doesn't exist yet.")

        # Setting Changing Loop
        while True:
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

if __name__ == "__main__":
    if DEBUG:
        sys.exit(main())
    else:
        try:
            sys.exit(main())
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)


