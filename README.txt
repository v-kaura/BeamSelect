To run, open terminal and change the active directory to the folder containing the python (".py") files. Then run the following command: "python beam_select.py". Alternatively, double click on "beam_select.py"
To set a condition, choose the appropriate column, comparison and value values and click "add condition". To remove a condition, select the condition in the list and click "remove condition".
Clicking "Find beams" after adding the conditions will print the beams that meet the criteria to the terminal window.

Notes:
- This program will work with Python 3 but (probably) not Python 2. If you're running Python 2 let me know and I'll put in the compatibility fixes for it. Alternatively, you'll have to download Python 3 to run it.

Changelog:
- Fixed behaviour for add and remove buttons. Once a condition is added, selecting it and clicking the remove condition button will remove it.
- Added list boxes on the tool window so that conditions and beams do not need to be shown on the terminal window at all.
- Added ability to filter by beam type