### FUNCTIONS ### 

# Prints the current data.
def printTracks(trackData, IDs):
    print("Here's what we've got: ")
    for key, value in trackData.items():
        print("[" + str(IDs.index(key)) + "] " + str(key) + ": " + str(value))

# Deals with poor user input.
def checkInput(userInput):
    # If input is empty, skip to next iteration.
    if userInput == "":
        return "empty"
        
    # If input is a decimal, print error and skip to next iteration.
    try:
        # If decimal = integer, pass
        if float(userInput) == float(int(float(userInput))):
            pass
            
        # Otherwise error
        else:
            return "decimal"
    except:
        pass

    try:
        # If input is negative, print error and skip to next iteration.
        if float(userInput) < 0:
            return "negative"
    except:
        pass 

    # Tries to convert input to an integer. 
    # If failed, converts string to title case and continues.
    try:
        return int(float(userInput))
        #print("Input successfuly converted to integer: " + str(track))
    except:
        return userInput.title()
        #print("Input could not be converted into integer, here's what we've got: " + str(track))

# Deals with errors.
def errorHandler(returnValue):
    if returnValue == "empty":
        return "You cannot enter an empty string."
    elif returnValue == "decimal":
        return "You cannot enter a decimal."
    elif returnValue == "negative":
        return "You cannot enter a negative number."
    else:
        return "all clear"
    