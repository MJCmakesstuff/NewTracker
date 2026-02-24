import json

# Loads tracks and tracksIndexes from JSON files.
with open("tracks.json", "r") as tracksJSON:
    tracks = json.load(tracksJSON)
#print("Loaded tracks: " + str(tracks))

with open("tracksIndexes.json", "r") as tracksIndexesJSON:
    tracksIndexes = json.load(tracksIndexesJSON)
#print("Loaded tracksIndexes: " + str(tracksIndexes))

while True:
    mode = input("What do you want to do? (add/remove): ")
    if mode == "add" or mode == "remove":
        while True: # Loop adding tracks until user exits.
            
            # Prints the current data.
            print("Here's what we've got: ")
            for key, value in tracks.items():
                print("[" + str(tracksIndexes.index(key)) + "] " + str(key) + ": " + str(value))

            userInput = input("What do you want to " + str(mode) + "? (type \"mode\" to change mode) ")
            if userInput == "mode":
                break
            else:
                track = userInput
            
            # If input is empty, skip to next iteration.
            if track == "":
                print("Exiting... please enter literlly any string")
                continue
                
            # If input is a decimal, print error and skip to next iteration.
            try:
                # If decimal = integer, pass
                if float(track) == float(int(float(track))):
                    pass
                    
                # Otherwise error
                else:
                    print("Decimals are not allowed, sorry :(")
                    continue
            except:
                pass

            # Tries to convert input to an integer. 
            # If failed, converts string to title case and continues.
            #print("Trying to convert input to integer...")
            try:
                track = int(float(track))
                #print("Input successfuly converted to integer: " + str(track))
            except:
                track = track.title()
                #print("Input could not be converted into integer, here's what we've got: " + str(track))

            # If input is integer (from previous try/except), tries to pull the corresponding item from tracksIndexes and set it as track.
            # If failed, that trackIndex doesn't exist, so print error and skip to next iteration.
            if type(track) == int:
                
                # If input is negative, print error and skip to next iteration.
                if track < 0:
                    print("Negative numbers are not allowed, sorry :(")
                    continue
                    
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






