CHANGELOG

03/14/2026 #2: Enhance settings management and user feedback with new reset feature and improved descriptions
- Added todo "Quit program, save or no save"
- Added the ability to reset the settings to their default values.
- Made the program more verbose and readable.
- Improved descriptions of possible settings options for when an invalid value is entered.
- (It's a lot of print() and time.sleep(0.1))
- Completed todo: "Add reset settings feature"
- Completed todo: "Better description of what values settings can be"



03/14/2026: Update settings and enhance input handling for tracking features
- Added todo: "Check if data is valid"
- Added the ability to use the multiplier setting implemented in the previous commit.
- Added todo: "Better description of what values settings can be"
- Completed todo: "Feature: add/sub by number. Like increase this one by 3."
- Added todo: "Add reset settings feature"



03/13/2026: The Settings Update
- Merged the following two subcommits to main branch.
- NOTE: "mode" setting does not currently have a use.

Subcommit #1 (03/13/2026): Settings Rework
- Created a settings file to store the "mode" and "multiplier" settings.
- Expanded the settings file to include a default value and information for checking if the setting is valid.
- Created a function to check if a value is acceptable for a given setting by using the rules specified in settings.json. This function only checks if the value is in an accepted values list, and passes on to the function I'll describe next if the value should be checked against certain rules rather than a list of accepted values.
- Created a function to check if an input follows certain rules. For example, "positive" or "integer". Should be easy to expand with more rules.
- Created todo: "Resolve "instance" tracebacks with the ruleChecker function."

Subcommit #2 (03/13/2026): New Settings Implementation
- Added a function to print the settings and their values with indecies in brackets (like with the tracks).
- Added todo: "Use the new "ruleChecker" function to simplify the other cases where we check for poor input."
- Modified the inputChecker to allow it to output both title and lower case depending on input.
- Added a "window" that allows the user to change settings.
- Modified the printSettings function to allow it to print settings with and without shortcut IDs, depending on input.
- Added some print() s to increase readabiliity.
- Fixed an issue where no error message would print for invalid input while chaning "mode" setting. 
- Added todo: "What to do when settings file doesn't exist, or is invalid?"
- Added todo: "Add error messages to new functions."
- Added /n s to CHANGELOG for improved readability.
- Completed todo: "Resolve "instance" tracebacks with the ruleChecker function."
- Completed todo: "Add error messages to new functions."
- Removed todo: "What to do when settings file doesn't exist, or is invalid?" Is it overprotection? Especially for the amount of time I belive it would take to resolve, I think so. Maybe I will come back to it.



03/11/2026: Remove tracksIndexes.json and "fix" .gitignore
- Fixed problems from mismatched tracks.json and tracksIndexes.json by obsolescing (?) tracksIndexes.json.
- The "tracksIndexes" variable is now generated using the data from tracks.json, thus ensuring they are "in sync."
- "Fixed" (or rather, modified in hopes of a solution) .gitignore.
- Ran "git rm -r --cached __pycache__" in hopes of removing that folder from being tracked.
- Completed todo: "BUG: what do we do when trackIndexes and tracks do not match? Bad things..."
- (Hopefully) completed todo: "BUG (?): Python cache seems to ignore the .gitignore..."



03/10/2026: Files and folders rework
- Added function to read data from a file, implemented accordingly.
- Added function to save data to a file, implemented accordingly.
- Create a "data" directory, set the paths of the data files to variables and make changes accordingly.
- Added a .gitignore for data and pesky .DS_Store
- Added todo: "BUG: what do we do when trackIndexes and tracks do not match? Bad things..."
- Added todo: "BUG (?): Python cache seems to ignore the .gitignore..."
- Removed todo: "Manage json file stuff. Like what to do if they're not there, or in the wrong format?"



03/04/2026 (second commit of the day, yikes haha)
- Made a function to handle the error message and enter to continue
- Removed the now obsolute enterToContinue function
- Completed todo: Improve error function



03/04/2026
- Added a function to press enter to continue, added to any error spots
- Changed some error messages
- Completed todo: "Make error messages more obvious."
- Added todo: "Improve error function"

02/28/2026
- Added changelog
- Added todo: address edge cases for storage files
- Made the following into functions rather than calling them repeatedly:
    - Printing data
    - Checking user input for empty strings, non-integer-equivalent decimals, and negative numbers. If successful, converts input to integer (if a number), or to title case (if a string).
    - Interpreting error messages from the "check user input" function.
- Created a file to store functions, modified main.py accordingly.
- Added todo: make error messages more obvious.
- Completed todo: Make things into functions because that's clean and nice