import time
import sys
import win32gui
import sqlite3
from datetime import datetime
import PySimpleGUI as sg
import threading

# Function to collect data of window names and timestamps
def backgroundTimer():    
    # Connect to the database
    db = sqlite3.connect('digitalWellbeing.db')
    dbCursor = db.cursor()

    # Get variables
    global oldProgramName
    global stopThread
    
    # Infinite loop to always run in the background
    while True:
        # Get (pointer and) name of current window in foreground
        windowPointer = win32gui.GetForegroundWindow()
        windowName = win32gui.GetWindowText(windowPointer)

        # Get program name from window name (use words after last dash) (excluding cmd)
        if windowName.startswith("Eingabeaufforderung") or windowName.startswith("Command Prompt"):
            activeProgramName = (windowName.split('-')[0]).strip()
        else:
            activeProgramName = (windowName.split('-')[-1]).strip()
            
        # If program changed (on first iteration: if no old program name exists) (don't save aeropeeks (with no window name))
        if activeProgramName != oldProgramName:
            # Get current datetime
            currentDatetime = datetime.now()
            
            if oldProgramName != "":
                # Update end time of last entry in table timeEntries
                dbCursor.execute('UPDATE timeEntries SET endTime = ? WHERE endTime IS NULL', (currentDatetime, ))

            if activeProgramName != "":
                # Insert program name and start time into table timeEntries
                dbCursor.execute('INSERT INTO timeEntries (entryName, startTime, windowName) VALUES (?, ?, ?)', (activeProgramName, currentDatetime, windowName))

            # Save changes to database
            db.commit()

            # Remember current program name for next iteration
            oldProgramName = activeProgramName

        time.sleep(1)

        if stopThread:
            break

# Function to collect last bit of data (endTime) when program is closed (by pressing "exit" button or closing the GUI window)
def backgroundTimerGUI(guiWindow):
    while True:
        guiEvent, guiValue = guiWindow.read()
        # If program is stopped by pressing the "exit"-button or by closing the GUI
        if guiEvent == "Exit" or guiEvent == sg.WIN_CLOSED:
            # Exit backgroundTimerGUI
            break

# "main" function
# Create and open window through PySimpleGUI
sg.theme('Dark')
layout = [
    [sg.Text("Collecting data")],
    [sg.Button("Exit")]
]
guiWindow = sg.Window("Digital Wellbeing", layout, margins=(150, 75))

# Initialize global variables
oldProgramName = ""
stopThread = False

# Run backgroundTimer function in seperate thread (for parallel work)
x = threading.Thread(target=backgroundTimer)
x.start()

# Run function to collect last bit of data (endTime) when program is closed
backgroundTimerGUI(guiWindow)

# Stop the program
stopThread = True

# Get current datetime
currentDatetime = datetime.now()

# Connect to the database
db = sqlite3.connect('digitalWellbeing.db')
dbCursor = db.cursor()

# Update end time of last entry in table timeEntries
dbCursor.execute('UPDATE timeEntries SET endTime = ? WHERE endTime IS NULL', (currentDatetime, ))

# Save changes to database
db.commit()

# Close the GUI
guiWindow.close()
