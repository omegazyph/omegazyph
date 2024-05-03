"""
Countdown Timer Application

This program creates a graphical user interface (GUI) for a countdown timer. 
Users can input hours, minutes, and seconds, and the program will countdown 
from the specified time. When the timer reaches zero, it displays a message 
and optionally plays a notification sound.

Author: wayne stock
Date: 2024-05-03
"""

# Import necessary libraries
import time
import tkinter as tk
from tkinter import *
from datetime import datetime
from win10toast import ToastNotifier
import winsound

# Function to initiate countdown
def countdown():
    # Get user input for hours, minutes, and seconds
    h = hour.get()
    m = minus.get()
    s = secon.get()
    # Calculate total seconds
    t = h * 3600 + m * 60 + s
    # Countdown loop
    while t:
        mins, secs = divmod(t, 60)
        display = ('{:02d}:{:02d}'.format(mins, secs))
        time.sleep(1)  # Sleep for 1 second
        t -= 1
        # Update display
        Label(window, text=display).pack()
    # Check if notification is enabled
    if check.get():
        winsound.Beep(440, 1000)  # Beep sound
    # Display "Time's Up" message
    Label(window, text="Time's Up", font=('bold', 20)).place(x=250, y=440)
    # Display notification on desktop
    toast = ToastNotifier()
    toast.show_toast("Notification", "Timer is Off", duration=20, icon_path=None, threaded=True)

# Create main window
window = Tk()
window.geometry('600x600')  # Set window size
window.title('PythonGeeks')  # Set window title
Label(window, text="Countdown Clock and Timer", font=('Calibri 15')).pack(pady=20)

# Display current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
Label(window, text=current_time).pack()

# Define variables for user input
check = tk.BooleanVar()
hour = tk.IntVar()
minus = tk.IntVar()
secon = tk.IntVar()

# User input for time
Label(window, text="Enter time in HH:MM:SS", font=('bold')).pack()
Entry(window, textvariable=hour, width=30).pack()
Entry(window, textvariable=minus, width=30).pack()
Entry(window, textvariable=secon, width=30).pack()

# Checkbox for enabling notification
Checkbutton(text='Check for Music', onvalue=True, variable=check).pack()

# Button to initiate countdown
Button(window, text="Set Countdown", command=countdown, bg='yellow').pack()

# Update window and run main loop
window.update()
window.mainloop()
