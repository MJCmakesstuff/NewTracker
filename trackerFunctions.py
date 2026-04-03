import json
import time

### FUNCTIONS ### 

# Prints the current data.
def printTracks(trackData):
    for index, (key, value) in enumerate(trackData.items(), start=1):
        print(f"[{index}] {key}: {value}")
    print()

# Deals with poor user input.
def checkInput(userInput, case=None):
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
        
        if case == "lower":
            return userInput.lower()
        else:
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
def errorMessage(message=""):
    if message != "":
        print(message)
    input("Press Enter to continue...")
    print()

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
        print(f"{fileName} doesn't exist or is corrupted. Creating a new one...")
        return fallback

# Saves data to a JSON file.
def saveData(data, fileName):
    with open(fileName, "w") as file:
        json.dump(data, file, indent=4)

# Checks if settings are valid
def checkSetting(setting, validType, validValues, inParams=None):
    defaultParams = {"verbose": True}
    if inParams is None:
        inParams = {}
    params = {**defaultParams, **inParams}
    
    
    #print(f"{setting} should be of type {validType} and follow these rules: {validValues}, params are: {params}")
    if validType == "set":
        if setting in validValues:
            return True
        else:
            #print(f"Verbose is set to {params["verbose"]}.")
            if params["verbose"]:
                #print("I AM RUNNING INSIDE CHECKSETTING")
                #print(params["verbose"])
                print("That isn't a valid option for that setting.")
                print("Valid options are: ")
                for value in validValues:
                    print(value)
                errorMessage()
            return False
    if validType == "rules":
        return ruleChecker(setting, validValues, {"verbose": params["verbose"]})

# Checks if a value follows certain rules (given function input)
def ruleChecker(value, rules, inParams=None):
    defaultParams = {"convertToInt": True, "verbose": True, "convertToBool": True}
    if inParams is None:
        inParams = {}
    params = {**defaultParams, **inParams}
    
    #print(f"Checking {value} against rules: {rules}...")
    for rule in rules:
        if rule == "integer":
            #print(f"Checking if {value} is an integer...")
            try:
                if int(value) == int(float(int(value))):
                    #print(f"{value} is equal as integer and float.")
                    if params["convertToInt"]:
                        #print("Instructed to convert to ingeter, converting...")
                        value = int(value)
                        #print(f"Converted to integer: {value}")

                    else:
                        #print("Instructed to not convert to integer, skipping...")
                        pass
                else:
                    #print(f"{value} is not equal as integer and float.")
                    if params["verbose"]:
                        print("This must be an integer.")
                        print("This must be:")
                        for rule in rules:
                            print(f" - {rule}")
                        errorMessage()
                    return False
            
            except ValueError:
                #print(f"{value} could not be converted to an integer or float.")
                if params["verbose"]:
                    print("This must be an integer.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            
            if not isinstance(value, int):
                #print(f"{value} is not an integer type.")
                if params["verbose"]:
                    print("This must be an integer.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
        
        elif rule == "positive":
            if not value > 0:
                if params["verbose"]:
                    print("This must be a positive number.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            
        elif rule == "non-empty":
            if value == "":
                if params["verbose"]:
                    print("This cannot be empty.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            
        elif rule == "string":
            try:
                value = float(value)
                if params["verbose"]:
                    print("This must be a string.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            except ValueError:
                try:
                    value = str(value)
                    if isinstance(value, str):
                        #return True
                        #Trying this instead...
                        pass

                except ValueError:
                    if params["verbose"]:
                        print("This must be a string.")
                        print("This must be:")
                        for rule in rules:
                            print(f" - {rule}")
                        errorMessage()
                    return False

        elif rule == "strict-non-string":
            if isinstance(value, str):
                if params["verbose"]:
                    print("This cannot be a string.")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False

        elif rule == "titleCase":
            #print(f"Checking if {value} is in title case...")
            #print(value)
            #print(value.title())
            if value != value.title():
                if params["verbose"]:
                    print("This must be in title case (first letter of each word capitalized).")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            else:
                #print(f"{value} is in title case.")
                pass

        elif rule == "boolean":
            if convertToBool(value) == "not bool":
                if params["verbose"]:
                    print("This must be a boolean (true/false).")
                    print("This must be:")
                    for rule in rules:
                        print(f" - {rule}")
                    errorMessage()
                return False
            else:
                if params["convertToBool"]:
                    value = convertToBool(value)

    return True

# Fixes the settings file if any of the settings are invalid (and saves!)        
def fixSettingsFile(settings, schema, save_location):
    for key, value in schema.items():
        #print(f"Checking setting '{key}' with value '{settings[key]}' against rules: {value['rules']}...")
        if checkSetting(settings[key], value["type"], value["rules"], {"verbose": False}):
            continue
        else:
            print(f"Invalid value for setting '{key}' found in settings.json. Resetting to default: {value['default']}...")
            settings[key] = value["default"]
    saveData(settings, save_location)

# Prints the current settings.
def printSettings(settings, options={"ids": True}):
    print("Here are the current settings: ")
    for index, (key, value) in enumerate(settings.items(), start=1):
        if options["ids"]:
            print(f"[{index}] {key}: {value}")
        else:
            print(f"{key}: {value}")
    print()

# Resets settings to their default values.
def resetSettings(settings, schema, save_location):
    for key, value in schema.items():
        settings[key] = schema[key]["default"]
    saveData(settings, save_location)
    print("Settings reset.")
    print()

# Tries to convert input to a boolean. If failed, retunrns "not bool".
def convertToBool(value):
    if str(value).strip().lower() in ["true", "yes", "1", "y", "t"]:
        return True
    elif str(value).strip().lower() in ["false", "no", "0", "n", "f"]:
        return False
    else:
        return "not bool"





