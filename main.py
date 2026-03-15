import json
import time
import trackerFunctions as funcs
from pathlib import Path

i = 0
while i < 5:
    print()
    i += 1

# Creates a "data" directory if it doesn't exist.
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Sets data files to vars
tracks_file = data_dir / "tracks.json"

# Loads tracks, tracksIndexes, and settings from JSON files.
tracks = funcs.loadData(tracks_file, {})
tracksIndexes = list(tracks.keys())
settings = funcs.loadData("settings.json", {})

# Saves the data (to prevent problems reading bad files)
funcs.saveData(tracks, tracks_file)

# Fixes the settings file if any of the settings are invalid.
funcs.fixSettingsFile(settings)
funcs.printSettings(settings, {"ids": False})

# Loop of Death
while True:
    if settings["mode"]["value"] == "add" or settings["mode"]["value"] == "subtract":
        while True:
            print()
            print("Here's what I'm tracking so far: ")
            funcs.printTracks(tracks, tracksIndexes)

            userInput = input("What do you want to " + str(settings["mode"]["value"]) + " by " + str(settings["multiplier"]["value"]) + "? (type \"settings\" to change settings) ")
            if userInput == "settings":
                print("Switching to settings window...")
                time.sleep(0.5)
                print()
                time.sleep(0.1)
                break
            else:
                track = funcs.checkInput(userInput)

            if funcs.errorHandler(track) != "all clear":
                funcs.errorMessage(funcs.errorHandler(track))
                continue
            
            # If input is integer, tries to pull the corresponding item from tracksIndexes and set it as track.
            # If failed, that trackIndex doesn't exist, so print error and skip to next iteration.
            if type(track) == int:
                try:
                    track = tracksIndexes[track]
                except:
                    funcs.errorMessage("That doesn't exist yet.")
                    continue
            
            # If the track exists, add 1.
            # Otherwise, create the track, and add it to the index list.
            if track in tracks:
                if settings["mode"]["value"] == "add":
                    tracks[track] += int(settings["multiplier"]["value"])
                    print("Added " + str(settings["multiplier"]["value"]) + " to " + str(track) + ". New value: " + str(tracks[track]))
                    time.sleep(0.5)
                    print()
                    time.sleep(0.1)

                elif settings["mode"]["value"] == "subtract":
                    tracks[track] -= int(settings["multiplier"]["value"])
                    if tracks[track] <= 0:
                        del tracks[track]
                        tracksIndexes.remove(track)
                        print("Removed " + str(track) + ".")
                        time.sleep(0.5)
                        print()
                        time.sleep(0.1)
                    
                    else:
                        print("Subtracted " + str(settings["multiplier"]["value"]) + " from " + str(track) + ". New value: " + str(tracks[track]))
                        time.sleep(0.5)
                        print()
                        time.sleep(0.1)

            else:
                if settings["mode"]["value"] == "add":
                    tracks[track] = int(settings["multiplier"]["value"])
                    tracksIndexes.append(track)
                    print("Created " + str(track) + " with value " + str(tracks[track]) + ".")
                    time.sleep(0.5)
                    print()
                    time.sleep(0.1)

                elif settings["mode"]["value"] == "subtract":
                    funcs.errorMessage("That doesn't exist yet.")
                    continue

            # Saves the data back to the JSON files.
            funcs.saveData(tracks, tracks_file)



    else:
        funcs.errorMessage("That doesn't exist yet.")

    # Setting Changing Loop
    while True:
        funcs.printSettings(settings)
        userInput = input("What setting do you want to change? (type \"done\" to finish, or \"reset\" to reset to defaults) ")
        if userInput == "done":
            print("Switching to main window...")
            time.sleep(0.5)
            print()
            time.sleep(0.1)
            break
        elif userInput == "reset":
            funcs.resetSettings(settings)
            continue
        else:
            setting = funcs.checkInput(userInput, "lower")
            if funcs.errorHandler(setting) != "all clear":
                funcs.errorMessage(funcs.errorHandler(setting))
                continue
        
        if type(setting) == int:
                try:
                    setting = list(settings.keys())[setting]
                except:
                    funcs.errorMessage("That doesn't exist yet.")
                    continue

        if setting in settings:
            newValue = input("What would you like to change " + str(setting) + " to? ")
            if funcs.checkSetting(newValue, settings[setting]["type"], settings[setting]["rules"]):
                settings[setting]["value"] = newValue
                funcs.saveData(settings, "settings.json")
                print("Changed " + str(setting) + " to " + str(newValue) + ".")
                time.sleep(0.5)
                print()
                time.sleep(0.1)

            else:
                continue
        else:
            funcs.errorMessage("That doesn't exist yet.")
            continue
