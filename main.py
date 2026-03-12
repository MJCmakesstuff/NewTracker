import json
import time
import trackerFunctions as funcs
from pathlib import Path

# Creates a "data" directory if it doesn't exist.
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Sets data files to vars
tracks_file = data_dir / "tracks.json"

# Loads tracks and tracksIndexes from JSON files.
tracks = funcs.loadData(tracks_file, {})
tracksIndexes = list(tracks.keys())

# Saves the data (to prevent problems reading bad files)
funcs.saveData(tracks, tracks_file)

# Loop of Death
while True:
    mode = input("What do you want to do? (add/remove): ")
    if mode == "add" or mode == "remove":
        while True:
            
            funcs.printTracks(tracks, tracksIndexes)

            userInput = input("What do you want to " + str(mode) + "? (type \"mode\" to change mode) ")
            if userInput == "mode":
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
                if mode == "add":
                    tracks[track] += 1
                elif mode == "remove":
                    tracks[track] -= 1
                    if tracks[track] <= 0:
                        del tracks[track]
                        tracksIndexes.remove(track)
            else:
                if mode == "add":
                    tracks[track] = 1
                    tracksIndexes.append(track)
                elif mode == "remove":
                    funcs.errorMessage("That doesn't exist yet.")
                    continue

            # Saves the data back to the JSON files.
            funcs.saveData(tracks, tracks_file)

    else:
        funcs.errorMessage("That doesn't exist yet.")






