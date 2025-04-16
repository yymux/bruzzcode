import tkinter as tk
import random

# ---------------------- MODULE 2 ----------------------
def createMap(bombNo): # Creates a map which the buttons reference when deciding what to do when clicked

    global bombCoordinates 

    for i in range(10): # Creates a 10x10 map of 0s
        mapx = []
        for j in range(10):
            mapx.append(0)
        map.append(mapx)
 
    for i in range(bombNo): #Creates x amount of bombs in random locations
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        bombCoordinates.append([y,x])
        map[y][x] = "X"
    
    for bomb in bombCoordinates: # For each bomb, update the surrounding cells to indicate the number of bombs around it
        y = bomb[0]
        x = bomb[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                ni, nj = y + i, x + j
                if 0 <= ni < 10 and 0 <= nj < 10:  # Ensure within bounds
                    if map[ni][nj] != "X":  # Only update if it's not a bomb
                        map[ni][nj] += 1 # Adds one to the number of bombs around it, allows for 0-8 bombs to be around it

    # --DELETE THIS BEFORE SHOWING BROWN--  Broken code (Keep the code to show iterative testing) (Can cause numbers on the map to be wrong) (Say you fixed it by replacing the try except thing with the ni nj stuff on line 25) 
    """
    for bomb in bombCoordinates:
        y = bomb[0]
        x = bomb[1]

        for i in range(-1, 2):
            for j in range(-1, 2):
                    try:
                        map[y+i][x+j]
                    except IndexError:
                        pass
                    else:
                        if map[y+i][x+j] != "X":
                            map[y+i][x+j] += 1
    """
                            
    for row in map: # Print the map for developer testing purposes
        print(row,end="")
        print("\n")

# --------------------- MODULE 2 ----------------------
    
def revealSpace(i, j): # Reveals the space when clicked, and checks if it is a bomb or not

    checkGameStatus()
    if flagMode: # If flag mode is activated, toggle the flag on the button
        if str(buttons[i][j]["text"]).isdigit(): # If the button is already revealed, end it
            return
        if buttons[i][j]["text"] == "F":# If the button is flagged, unflag it
            buttons[i][j].config(text=" ", bg="lightgrey")
        else: # If the button is not flagged, flag it
            buttons[i][j].config(text="F", bg="yellow")
        return
    
    else: # If flag mode is not activated, reveal the space

        if buttons[i][j]["text"] != " ": #Checks if the button is already revealed, ends if so
            return

        # Starts the game over process if the button is a bomb
        if map[i][j] == "X":
            buttons[i][j].config(text="X", bg="red")
            gameOver()
            return
        
        else: # If not, use the map to sbow the number of bombs around it,if any
            buttons[i][j].config(text=map[i][j], bg="white")

        # If the current space is 0, reveal all adjacent spaces
        if map[i][j] == 0:
            for k in range(-1, 2):
                for l in range(-1, 2):
                    ni, nj = i + k, j + l
                    if 0 <= ni < 10 and 0 <= nj < 10:  # Ensure within bounds
                        revealSpace(ni, nj) # Repeats the process until the space to be revealed is not 0

def checkGameStatus(): # Checks if the game is over by checking if all the bombs are flagged

    win = True 
    for bomb in bombCoordinates:
        y = bomb[0]
        x = bomb[1]
        if buttons[y][x]["text"] != "F":
            win = False
            break
    
    if win:
        description.config(text="You win! Press r to reset.") # Changes the description to show win message and disables the buttons
        for i in range(len(buttons)): 
            for j in range(len(row)):
                buttons[i][j].config(state="disabled")

def gameOver(): # Ends the game when the bomb is found.

    for i in range(len(buttons)): # Reveals all the buttons when the game is over
        for j in range(len(row)):
            if buttons[i][j]["text"] != "X":
                buttons[i][j].config(text=map[i][j],bg="white")
            else:
                buttons[i][j].config(text="X", bg="red")
            button.config(state="disabled") # Disables the buttons to prevent further clicks

    description.config(text="Game Over! Press r to reset.") # Changes the description to show game over message

def openHelp(event): # Opens the help window when the help button is clicked

    def closeHelpWin():
        global helpOpened
        helpOpened = False # Sets the help window to closed
        helpWindow.destroy() # Destroys the help window
        
    global helpOpened # Declare the global variable
    if helpOpened: # If the help window is already opened, do nothing
        return
    else:
        helpWindow = tk.Toplevel(root) # Creates a new window
        helpWindow.title("Help") # Sets the title of the help window
        helpText = tk.Label(helpWindow, text="Instructions:\n\n1. Click on a square to reveal it.\n2. If you click on a bomb, the game is over.\n3. If you click on a square with no bombs around it, all adjacent squares will be revealed.\n4. Use flag mode (space) to mark squares as bombs.\n5. Press 'r' to reset the game.").pack() # Creates the help text
        closeBtn = tk.Button(helpWindow, text="Close", command=closeHelpWin).pack() # Creates the close button
        helpOpened = True # Sets the help window to opened

def restart(event): # Resets the game when space is pressed after game over

    global map, buttons, flagMode, bombCoordinates # Declare the global variables
    map = [] # Resets the map
    flagMode = False # Resets the flag mode
    bombCoordinates = [] # Resets the bomb coordinates
    for button in buttons: # Resets the buttons
        for b in button:
            b.config(text=" ", bg="lightgrey", state="normal")

    description.config(text="Flag mode is disabled") # Resets the description label
    createMap(BOMB_NUMBER) # Creates a new map with 13 bombs

root = tk.Tk() # Creates the main window, and sets the title and description label
root.title("Minesweeper")
description = tk.Label(root, text="Flag mode is disabled bruzz") # Creates the description label
description.grid(row=10, columnspan=10) # Position the label below the buttons for visibility
map = [] # List to store the map
buttons = [] # List to store the buttons
flagMode = False # Flag mode is disabled by default
keyPressed = False  # Flag to track if the key is already pressed
BOMB_NUMBER = 5 # Default number of bombs
bombCoordinates = [] # List of bomb coordinates
helpOpened = False # Flag to track if the help window is already opened

def toggleFlag(event): # Allows the user to toggle flag mode on and off by pressing the space key

    global flagMode, keyPressed # Declare the global variables
    if not keyPressed:  # Only toggle if the key is not already pressed
        keyPressed = True 
        flagMode = not flagMode # Changes the flag mode from true to false, or false to true
        if flagMode: #Update the description label based on the flag mode status
            description.config(text="Flag mode activated. ")
        else:
            description.config(text="Flag mode deactivated.")

def resetKey(event): # Stops the flag from being toggled multiple times when the key is held down

    global keyPressed
    keyPressed = False  # Reset the keyPressed flag when the key is released

# -------------------- MODULE 1 --------------------
for i in range(10): # Creates the buttons and adds them to the grid
    row = [] 
    for j in range(10): # Creates 10 buttons in each row
        button = tk.Button(root, text=" ", width=3, height=1,bg="lightgrey") # Creates the button with a light grey background
        button.config(command=lambda i=i, j=j: revealSpace(i, j)) # Sets the command to reveal the space when clicked
        button.grid(row=i, column=j) # Adds the button to the grid
        row.append(button) 
    buttons.append(row)
#--------------------- MODULE 1 ----------------------

# ------------------- MODULE 3 ----------------------
root.bind("<space>", toggleFlag)  # Press 'a' to create a map with 10 bombs
root.bind("<KeyRelease-space>", resetKey)  # Reset the keyPressed flag on key release
root.bind("r", restart) # Allows the user to restart the game by pressing space
root.bind("<KeyRelease-r>", resetKey)  # Reset the keyPressed flag on key release
root.bind("<h>", openHelp) # Press F1 to open the help window
root.bind("<KeyRelease-h>", resetKey) # Press F2 to create a map with 13 bombs
#------------------- MODULE 3 ----------------------

createMap(BOMB_NUMBER) # Creates the map with 13 bombs
root.mainloop() # Allows the window to run until closed