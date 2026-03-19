CHANGELOG

03/19/2026 #2: Refactor track management in main.py by implementing addTrack and subtractTrack methods; update README and CHANGELOG to reflect changes.
- Renamed some symbols.
- Moved the logic in main() that differentiates between increasing a track and creating a track into TrackList.add(self, track, multiplier).
- Did the same for decreasing and removing: combined into TrackList.subtract(self, track, multiplier).
- TrackList.add() and .subtract() now return True or False (in case .subtract() tries to delete a track that doesn't exist).
- Removed all the now obsolete logic and replaced with my_list.add() and .subtract().
- Completed todo: "Move delete track logic into subtract function and create track logic into add function."



03/19/2026: Update CHANGELOG and README with new todos; refactor main.py to utilize TrackList methods for track management
- initializeData() no longer returns data_dir (as it was unused in main()).
- initializeData() now returns my_list rather than my_list.data and my_list.ids.
- Replaced all instances of tracks with my_list.data and tracksIndexes with my_list.ids.
- Replaced all instances of adding, subtracting, creating, or deleting a track with the my_list functions.
- Instances of saving tracks now use my_list.save(tracks_file).
- Added todo: "Move delete track logic into subtract function and create track logic into add function."
- Added todo: "Call save function after add/subtract functions, and generate ids as well."
- Completed todo: "implement class changes for tracks to main()."


03/18/2026 #2: Implement TrackList class for improved track management; update README and CHANGELOG with new features and todos
- Created a class for tracks. It's a dictionary. It can load from a file, save to a file, validate the data in itself, generate ids for the keys in its data, print itself along with the ids, increase and decrease tracked items, as well as create and delete tracked items.
- Changed instances in initalizeData() where any of the above were done for the variable "tracks" to use the class instead for "my_list" subject to change.
- Added todo: implement class changes for tracks to main().
- NOTE: despite main remaing unchanged, the program still works (I think).
- Added todo: "Ability to have multiple lists of tracks using the new class"
- Added todo: "Make settings into a class as well"



03/18/2026: Enhance main.py with structured error handling, debug mode, and improved function organization; update CHANGELOG and README.md
- Put everthing in main.py into a main() functions, then added if __name__ == "__main__": sys.exit(main()) at the end.
- Created a separate function within main.py for initializing data. This function is later called in main() and all the variables are set to what they were in the initialize function.
- Completed todo: "What the heck does this mean and should I do something with regards to it? if __name__ == '__main__': sys.exit(main())"
- Added a DEBUG variable. If true, main() runs as usual. Otherwise, main() runs inside a try block, and a traceback gets printed and runs sys.exit(1).
- Changed the symbol for trackerFunctions from funcs to tf for simplicity. (I was amazed at how easy VSCode makes this!)



03/17/2026 #3: Add welcome message, exit option, and update input prompts in main.py; update CHANGELOG and README.md
- Added todo: "What the heck does this mean and should I do something with regards to it? if __name__ == '__main__': sys.exit(main())"
- Added welcome greeting and exit sendoff.
- Added the ablity to exit the program from the settings window by typing "quit".
- Completed todo: "Quit program, save or no save"
- Note: the program autosaves throughout so I did not implement an option to save/not save on quitting.



03/17/2026 #2: Refactor settings management by implementing a schema, enhancing input validation, and migrating settings storage to a variable. Remove settings.json and update related functions for improved handling.
- Added a settings schema in main.py to contain the settings, their default values, and allowed values.
- settings.json now only stores settings values.
- Modified main.py and resetSettings, fixSettingsFile, and printSettings in trackerFunctions.py to reflect these changes.
- Fixed some printing issues resulting from the previous changes.
- Rewrote functions involving the "params" input. Now, the default value is None, and at the beginning of the function the default params are specified and then merged with the inputted parameters (overwriting defaults).
- Parts of the code that saved to settings.json now save to a variable called settings_file, so I can change it's location in one spot.
- Moved settings.json to the data folder.
- Completed todo: "Input validation for files (important): what do I do if the settings file doesn't exist?"



03/17/2026: Enhance settings management by adding boolean input validation and conversion
- Added a rule to ruleChecker to check if input is a boolean (ex. 1, yes, true all = True).
- User can now change settingsPersist from the settings window.
- Completed todo: "Make it possible to change settingsPersist from settings window."



03/16/2026: Enhance input validation and settings management with new rules and checks
- Added todo: "Input validation for files (important): what do I do if the settings file doesn't exist?"
- Added todo: "Classes (object-oriented design): I don't know what this means yet but someone said I should do it."
- Added todo: "Eventually add unit tests. Again, whatever that means..."
- Built code to check if the data in tracks.json is valid.
- Added parameter input to the ruleChecker function. That way, I can have the function check if an input is an integer, and then based on the params decide whether to convert it to an integer (for example, 2.0), or just return True.
- Added more checking abilities to the ruleChecker function: does input contain something other than an empty string? Is the input a string that isn't a number? Is the input strictly a string (yes, in the case of "2", but not 2).
- Made loadData a bit more verbose
- Tweaked the printTracks function to account for the case where a boolean is stored in tracks.json (Surprise! It's 1s and 0s!)
- Added another parameter to ruleChecker: to print, or not to print. NOTE: there is a very real chance I broke something while making this change, and have not noticed it yet.
- Completed todo: "Check if data is valid" This is always an ongoing thing, so if I notice I make a change that results in more of these problems I'll probably add it back to the todo.
- Added a settingsPersist option. If false, the settings wipe on startup (settingsPersist resets to true).
- Added todo: "Make it possible to change settingsPersist from settings window."
- Probably more I forgot to write down. This was pretty hectic and all over the place in terms of bugfixing/tweaking.
- SIDE NOTE: ruleChecker function now takes up 139 (mental math) lines. 2-3 more options for rules to check, and it'd be longer than main.py!



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