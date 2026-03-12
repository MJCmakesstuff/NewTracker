CHANGELOG

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