import json
import time

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

# Error message thing
def errorMessage(message):
    print(message)
    time.sleep(1)
    input("Press Enter to continue...")

# Loads data from a JSON file.
def loadData(fileName, fallback):
    try:
        with open(fileName, "r") as file:
            data = json.load(file)
            if isinstance(data, type(fallback)):
                return data
            else:
                return fallback
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback

# Saves data to a JSON file.
def saveData(data, fileName):
    with open(fileName, "w") as file:
        json.dump(data, file, indent=4)

# Checks if settings are valid
def checkSetting(setting, validType, validValues):
    if validType == "set":
        if setting in validValues:
            return True
        else:
            return False
    if validType == "rules":
        return ruleChecker(setting, validValues)

# Checks if a value follows certain rules (given function input)
def ruleChecker(value, rules):
    for rule in rules:
        if rule == "positive":
            if not value > 0:
                return False
        elif rule == "integer":
            if not isinstance(value, int):
                return False
            
        # Continue adding more rules as needed
    
    return True

# Fixes the settings file if any of the settings are invalid (and saves!)        
def fixSettingsFile(settings):
    for key, value in settings.items():
        if checkSetting(value["value"], value["type"], value["rules"]):
            continue
        else:
            value["value"] = value["default"]
    saveData(settings, "settings.json")






