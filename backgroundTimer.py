import time
import win32gui
import sqlite3
from datetime import datetime
import PySimpleGUI as sg
import threading

import loadingGif

# Function to collect data of window names and timestamps
def backgroundTimer():    
    # Connect to the database
    db = sqlite3.connect('digitalWellbeing.db')
    dbCursor = db.cursor()

    # Get variables
    global oldProgramName
    global stopThread
    global name_of_subject

    # Infinite loop to always run in the background
    while True:
        # Get name of current window in foreground
        windowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())

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
                dbCursor.execute('INSERT INTO timeEntries (entryName, subject, startTime, windowName) VALUES (?, ?, ?, ?)', (activeProgramName, name_of_subject, currentDatetime, windowName))

            # Save changes to database
            db.commit()

            # Remember current program name for next iteration
            oldProgramName = activeProgramName

        time.sleep(1)

        if stopThread:
            break

# Function to collect last bit of data (endTime) when program is closed (by pressing "exit" button or closing the GUI window)
def backgroundTimerGUI(guiWindow):
    global name_of_subject

    while True:
        guiEvent, guiValue = guiWindow.Read(timeout=25)

        if guiEvent == "Exit" or guiEvent == sg.WIN_CLOSED:
            if sg.popup_yes_no("Are you sure you want to exit?") == 'Yes':
                break
        elif guiEvent == "GBI" or guiEvent == "LA1" or guiEvent == "Proggen 1" or guiEvent == "Proggen 2":
            name_of_subject = guiEvent
            guiWindow['info-text'].update(guiEvent)
        elif guiEvent == "Reset subject":
            name_of_subject = "no subject"
            guiWindow['info-text'].update("no subject")
        guiWindow['gif'].UpdateAnimation(loadingGif.get_gif(), time_between_frames=20)

# "main" function
# Initialize global variables
oldProgramName = ""
stopThread = False
name_of_subject = "no subject"

# Create and open window through PySimpleGUI
sg.theme('Dark')
layout = [
    [sg.Text("Collecting data..."), sg.Image(loadingGif.get_gif(), key='gif')],
    [sg.Button("GBI"), sg.Button("LA1"), sg.Button("Proggen 1"), sg.Button("Proggen 2"), sg.Button("Reset subject")],
    [sg.Text("current selected subject:"), sg.Text("no subject selected", key='info-text')],
    [sg.Button("Exit")]
]

guiWindow = sg.Window("Digital Wellbeing", layout, element_justification='c', grab_anywhere=True, icon=r'C:\Users\Thomas2\bwSyncShare\DigiTime_GitHub\DigiTime-main\static\logo.ico')

# Run backgroundTimer function in seperate thread (for parallel work)
x = threading.Thread(target=backgroundTimer)
x.start()

# Run GUI
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
