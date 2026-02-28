import json
import trackerFunctions as funcs

# Loads tracks and tracksIndexes from JSON files.
with open("tracks.json", "r") as tracksJSON:
    tracks = json.load(tracksJSON)

with open("tracksIndexes.json", "r") as tracksIndexesJSON:
    tracksIndexes = json.load(tracksIndexesJSON)

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
                print(funcs.errorHandler(track))
                continue
            
            # If input is integer, tries to pull the corresponding item from tracksIndexes and set it as track.
            # If failed, that trackIndex doesn't exist, so print error and skip to next iteration.
            if type(track) == int:
                try:
                    track = tracksIndexes[track]
                except:
                    print("We don't have antying with that number, sorry :(")
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
                    print("I'm not tracking that, so I can't remove it.")
                    continue

            # Saves the data back to the JSON files.
            with open("tracks.json", "w") as tracksJSON:
                json.dump(tracks, tracksJSON, indent = 4)

            with open("tracksIndexes.json", "w") as tracksIndexesJSON:
                json.dump(tracksIndexes, tracksIndexesJSON, indent = 4)

    else:
        print("Sorry, we don't have that option yet :(")






