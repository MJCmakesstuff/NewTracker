CHANGELOG

07/06/2026: Add goal progress fraction display
- Goal progress also displays as a fraction. For example, 1/50 (2%) rather than just the percentage. 
- calculate_goal_progress and construct_progress_bar can still work with just a percentage input, but now also can take a list: [running_total, goal_value] in order to display the fraction. 



07/05/2026: Add progress bar visual for goal progress
- Fixed the goal viewer so that it displays the goal's end time as a date rather than a timestamp. 
- Added a setting for whether to show goal progress when viewing track lists.
- Created a function which calculates goal progress as a decimal.
- statTimeDisplay now defaults to the "human" setting (YYYY-MM-DD HH:MM:SS.SSSSSS) to be consistent with the parts of the program that do not yet support different statTimeDisplay settings.
- Created a function which takes a decimal and creates a progress bar visual.
- User must now press Enter to continue after viewing goals.
- When viewing a list, items with goals show the goal values with progress bar and percentage.



06/19/2026: Add choice for goal end-time
- User can now specify an end time for a goal. Say, track this item 10 times within 7 days.
- - This will be used for tracking goal progress (am I on track?) and completion (did I do it in time?).



06/18/2026: Add basic goal viewing
- The user can now view the goals they've set. The program shows the goal value, start time, and end time.
- - I know this isn't a huge commit; I wanted to get myself going again on this, since I haven't been coding due to vacation and surgery. 



05/29/2026 #2: Add deleting goals
- Changed the add_goal function so that new lists and items are only added to goals.json at the very end. This prevents empty lists or items in goals.json.
- Added the ability for the user to delete goals.
- When goals are deleted, the program checks for and deletes empty stuff. If an item has no more goals, it is removed from goals.json. If a list has no more items with goals, it is also removed from goals.json.



05/29/2026: Add adding goals
- Added a goals window for the user to view goals, create goals, and delete goals.
- Added placeholder functions for these three tasks.
- User can now create goals. The user chooses an item in a list to create the goal for, and the amount the goal is. The program records the date the goal was created, a placeholder for me to implement timed goals, and the value.
- Multiple goals can be created for items.



05/27/2026 #2: Fix bugs in statistics viewing window
- Fixed problems in the statistics viewing window similar to those from the past commit.
- Fixed a bug in the statistics viewing window where the program would count all changes to an item in the running total, even if those changes occured outside the specified seach window.
- - The program now only running-totals changes within the specified search window.



05/27/2026: Fix bugs in statistics settings changing window
- Fixed "back" options in the statistics settings changing window. The program now correct travels back to the correct window when the user wishes.
- Fixed some scenarios where choices made in sub-windows could unintentionally affect other sub-windows.



05/25/2026 #3: Add ability to change stat settings within stat window, with assistance and explanations; Refactor stat magic strings
- Added the ability to change statTimeDisplay within the Statistics window, with explanations for each item.
- Added the ability to change statTimeWindow within the Statistics window. The user can pick a unit of measurement (days, months, years, etc.), and input the number of those they would like statTimeWindow to be. Then it multiplies by predetermined values to convert to seconds and stores in statTimeWindow.
- Changed "human", "timestamp", and "relative" into variables defined at the beginning of the program, to avoid the magic string problem. These variables represent the statTimeDisplay setting, and are used throughout the Statistics class.



05/25/2026 #2: Change statistics time display to accomodate settings
- Statistics window now displays times differently depending on settings:
- - "human": displays times as year-month-day hour:minute:second
- - "timestamp": displays times as timestamps
- - "relative": displays times as days since today, rounded to two decimals.



05/25/2026: Add all-time statistics option
- User can now see all modifications for a list by setting statTimeWindow to 0.
- Stats window now specifies how many days the search window is, but still displays the starting date.



05/22/2026 #2: Add basic statistics viewing
- Added a Statistics window
- Added two settings: one to control how far statistics searches, another for whether to display timestamps or human-readable times.
- Added the ability to see stats for a list. Displays all changes in a list since in within the timespan specified by statTimeWindow.
- - Displays list time first modified and
- - last modified,
- - items times modified and
- - change at that time, and
- - total change over timespan for item.
- NOTE: rush commit. Not super thoroughly tested, and more features are on the way.


05/22/2026: Implement statistics for individual tracks
- Lists are no longer deleted from statistics.
- Lists in statistics are no longer created when their counterparts are created. Instead, the program simply checks and creates if necessary whenever a list is edited.
- Tracked items are now tracked (how else do I say this???) in statistics. Stats remembers each modification to an item, recording the time it happened and the amount changed by. For deleting items this change is the negative previous value. So adding all these changes should (I think) result in the item's current value.



05/20/2026: Create Statistics class and implement basic functions
- Created a Statistics class. 
- Statistics can now be loaded and saved from json.
- When a new list is created, a dictionary is created and stored for that list. This dictionary currently remembers the time the list was created.
- When a list is deleted, this dictionary is also deleted.



05/15/2026 #2: Add backout option for importing/exporting/deleting
- Added the ability for the user to back out of importing/export from CSV and from deleting a list, with warning messages.
- User can now back out of deleting a list (or rather, choosing a list to delete).



05/15/2026: Fix more CSV import bugs
- Fixed a glaringly obvious bug where importing from csv only imports the last item.
- Fixed another bug that appeard out of nowhere where all imported values were "invalid" because the item values were imported as strings and not converted.



05/11/2026: Fix bug importing from csv with csv file
- Removed some debug prints and obsolete code.
- Added a try/except block for importing from CSV when no CSV file exists.



04/27/2026 #2: Add import from csv
- Added the ability to import data from a csv file.
- Loading the ListManager now clears its data (previously expected to only load once, changes account for loading during imports).


04/27/2026: Add export to csv
- Removed some modules no longer in use.
- Added the ability to export data to a csv file.



04/18/2026: Add "Other Actions" window
- Added a new window "Other Actions" to the main window.
- User can now reset settings and quit the program from this window.
- User can no longer reset settings from the settings window or quit from the main window. These actions must now be done from the other actions window.



04/11/2026: Implement Pydantic for settings validation
- Added Pydantic to validate settings, rather than by using manual validation. This includes the following changes/implementations:
- Created a new Settings() class which is a Pydantic thing. 
- It contains the rules for types that the settings are allowed to be as well as a validator for 'mode'. 
- SettingsManager() now extracts json from storage and unpacks it into Settings() for validation. 
- Resetting settings is now as simple as self.data = Settings()
- settings.fix() is no longer needed and was removed.
- tf.checkSetting() is no longer needed and was removed.
- tf.fixSettingsFile() is no longer needed and was removed.
- Rather than checking the new setting value against the rules in the settings schema, the program extracts the data from the settings class, changes the value, and then creates a "new" instance of Settings() to validate. 
- Updated some error messages to work with pydantic errors.
- More stuff I probably forgot.



04/07/2026: Improve file read/write error handing
- Added/modified try/except blocks around saving/loading files to account for other errors. 



04/04/2026 #3: Add type annotations
- Added type annotations for most of the functions. Might not ever be complete, but I'll keep them in mind going forward.



04/04/2026 #2: Fix zero bug
- Fix bug. User can no longer add to the last item in the list by entering "0." Previously I accounted for this by not allowing negative numbers, but then I changed the indexing to start at 1 so 0 was still allowed but became effectively negative.



04/04/2026: Add functionality to prevent duplicate list creation and allow users to back out of opening a list
- User can now back out of opening a list. Say, if they accidentaly try to open a list, but decide they would rather create or delete one.
- User can no longer create a list if a list with that name already exists.



04/03/2026 #3: Refactor magic strings into constants for improved code clarity and maintainability
- Removed some debug prints.
- Added an error message that I thought already existed.
- Removed some "magic strings." I don't really understand why this is better yet, but I was told to try it. I'll probably be better about these "magic strings" when I start something new or change a bunch more stuff.



04/03/2026 #2: Add _print_validation_error function for improved user feedback on validation rules
- Created _print_validation_error(rules) helper function which iterates through the rules and states them so the user knows what they are allowed to put.



04/03/2026: Remove time.sleep() calls for improved user experience and responsiveness.
- Removed time.sleep() calls for better experience.



03/31/2026: Implement data validation in ListManager and TrackList; remove invalid entries from loaded data.
- The program now checks for invalid data in all of tracks.json, rather than just the values in the kv pairs.



03/28/2026: Remove debug prints; eliminate self.fileLocation from TrackList class for cleaner code.
- Removed some debug prints.
- Removed the self.fileLocation from the TrackList class.



03/25/2026: Refactor main application structure by introducing App class; consolidate ListManager and SettingsManager, and enhance settings handling.
- Created an app class that contains what was previously "manager" and "settings" objects. Now I can pass app rather than both of those.
- Moved the list manager window and settings manager window inside of the new app class. They now refer to self rather than app.
- Moved the track editor window into the ListManager class.
- Moved initializeData to __init__ in App and main into App.



03/21/2026 #4: Add SettingsManager class for improved settings management and refactor related functions
- Created a SettingsManager class. It can load and save itself, reset to default, fix broken settings, and print itself.
- Changed some related functions accordingly.
- Completed todo: "Make settings into a class as well"
- Completed todo: "Classes (object-oriented design): I don't know what this means yet but someone said I should do it."



03/21/2026 #3: Refactor printTracks and list display for consistent ID printing and improved user experience. 
- Any time a list of choices is printed out, with the shortcut number in brackets, it now starts at one.
- It used to be inconsistent from place to place, somteimes starting at 1, other times at 0.



03/21/2026 #2: Update CHANGELOG and README for recent refactoring; eliminate self.ids in ListManager and update printTracks function for improved data handling.
- Eliminated self.ids list for both the TrackList and ListManager class. self.generateIDS is also no longer needed.
- Changed tf.printTracks() to accomodate. It now only accepts one input (data rather than data, ids), and uses enumerate(data) to find index.
- Instances where self.ids is needed now use a similar structure using enumerate().
- Completed todo: "Make self.ids obsolete in favor of the new "options" thing I've been using recently."



03/21/2026: Update CHANGELOG and README for recent list management enhancements; refactor ListManager methods for improved list creation and deletion functionality in main.py.
- This was a super chaotic session. Everything was super disjointed and all over the place, and I'm just now trying to remember what I just did. So apologies if I can not recall everything.
- User can now create and delete lists from the list management window. 
- Modified the functions to delete and create lists in the ListManger class. Now they can ask the user which list they would like to create/delete and then proceed to do it.
- - The logic would have worked just as well elsewhere, but this way simplified the option choosing process and may end up being better down the line.
- Fixed an error that has been the bane of my existence. When creating a new TrackList, I used the parameter (data={}). I had no idea that this would use the same dictionary for any track lists created in a session. Now I used (data=None) and create a new dictionary inside the actual function if data == None. Shoutout to ChatGPT for helping me solve this issue, I would have never figured this out otherwise.
- Completed todo: "Ability to have multiple lists of tracks using the new class"
- Added todo: "Make self.ids obsolete in favor of the new "options" thing I've been using recently."



03/20/2026 #2: Update CHANGELOG with new list management features; implement openList function in ListManager and refactor main.py for improved user navigation.
- Track editor now references an inputted variable "currentList" and passes that into whatever it's doing rather than using "My List" which I had put in temporarily.
- Created a window for managing lists.
- User can now open lists from the list managing window. They can no longer open lists from the main window and must go through the list managing window.
- Created a function in the ListManager class to open a list by printing the existing lists, asking the user which they'd like, and calling the track editing function.



03/20/2026: Update CHANGELOG and README for recent ListManager enhancements; refactor main.py to improve list management and data handling.
- Completed todo: "Clean up quitting and switching between windows for clarity."
- - This was actually accomplished in the previous commit, but I forgot to delete the todo.
- Removed TrackList.save() save location parameter. It now just saves to whatever location is specified as self.fileLocation.
- ListManager class now has a built in save location so I don't have to pass it.
- ListManager class now has functions to load, save, generate IDs, and print itself.
- ListManager now saves only the names of lists and their contents, but loads that data and creates a TrackList for each named list.
- The list of tracked items "My List" is now managed through "manager", an instance of the ListManager class. 
- "manager" stores instances of the TrackList class inside of itself.



03/19/2026 #6: Update CHANGELOG with recent changes; modify user prompts in main.py for improved clarity and navigation.
- Improved user ability to switch between windows.
- Removed the ability to quit from the settings window.
- Yeah I can't lie this is not a huge commit.



03/19/2026 #5: Update CHANGELOG and README with new todos; set DEBUG to False in main.py and refactor main function for improved structure and clarity.
- Added todo: "Make an "app" class so I don't have to pass everything everywhere."
- Turned the settings window and track window into their own functions, which are called within a loop in main.
- Added the ability for the user to switch between windows via a third, "main menu" window.
- Added the ability for the user to quit the program from the main menu.
- Added todo: "Clean up quitting and switching between windows for clarity."



03/19/2026 #4: Implement ListManager for enhanced list management; update TrackList to support naming and refactor main.py for integration; revise README and CHANGELOG to reflect new features and todos.
- TrackList class now has a name that can be set with TrackList(name).
- Created a ListManager class that can create lists and return existing ones.
- Data initializer and main now utilize the new ListManager class. 
- NOTE: This is a smaller commmit because I realize I need to make a better "window" management system in order to do anything meaningful. How can proceed developing the ability to have multiple lists if the user can't manage them yet?



03/19/2026 #3: Refactor TrackList methods to improve functionality; rename addTrack and subtractTrack to add and subtract, incorporate saving and ID generation, and update CHANGELOG and README accordingly.
- Removed TrackList.removeTrack() and .createTrack() as their logic (1 line) is now incorporated into .addTrack() and .subtractTrack().
- Renamed TrackList.addTrack() to .add and .subtractTrack() to .subtract.
- TrackList now sets self.fileLocation = Path("data") / "tracks.json" so it can save from inside itself. Maybe this will be more useful when I begin having multiple lists.
- TrackList.add() and .subtract() now call self.save() and .generateIDS() at the end.
- Instead of immediately returning True/False, .add() and .subtract() set the bool to a var which is returned after saving.
- Removed instances of changing the track IDs manually. It is all done with TrackList.generateIDS() now.
- Completed todo: "Call save function after add/subtract functions, and generate ids as well."



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