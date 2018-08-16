# Tkinter_Treasure_Hunter
A simple clicking game that was initially inspired by John Harper's Udemy Course "The Ultimate Tkinter Course: GUI for Python Projects". Thanks to a great deal of architectural coaching from James A Crabb (Git:jacrabb), the game became an exercise in developing apps using the MVC architecture. 

# Current Features: 
 - Model, View, Controller architecture
 - Tkinter GUI
 - Difficulty setter: Changes the size of the window, resets the target coordinate
 - HUD: Click coordinates and distance from target coordinate updated dynamically
 - Display Clicks Option: "Draws" clicks on the canvas using a grey gradient that represents proximity to target coordinates
 - Increase Search Radius Option: By default, you must click within 5 pixels of the target to "win".  This button increases the search radius by 5. The display clicks option will represent the larger search area accordingly. 
 - New Game Option: Available only after the target has been "found". This button covers up the HUD and launches a new game.
 
 # Future Features: 
 - A more tasteful implementation of the Model, View, Controller architecture
 - Remove the current difficulty from the difficulty selector option list.
 - Apply styles to the window
 - Use a sand-like image for the background, switch the image out upon difficulty changes
 - Include a more appropriate favicon than a smiley face
 - Include a label next to the "Increase Winning Radius" button that lists the current winning radius
 - When the "treasure" is found, draw a treasure chest on the screen at the target coordinates. 
 - Keep track of winners in a SQL database, display top winners in the current difficulty setting upon victory. 
