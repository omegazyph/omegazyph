# Countdown Timer Application
# This program creates a graphical user interface (GUI) for a countdown timer.
# Users can input hours, minutes, and seconds, and the program will countdown
# from the specified time. When the timer reaches zero, it displays a message
# and optionally plays a notification sound.
# Author: Wayne Stock
# Date: 2024-05-03

# imports
import time
import tkinter as tk
from tkinter import *
from datetime import datetime
from win10toast import ToastNotifier
import winsound


# Define background color variables
bg_color = 'black'
fg_color = 'white'
btn_color = 'lightblue'


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
        display = '{:02d}:{:02d}'.format(mins, secs)
        
        # Update display
        timer_label.config(text=display)
        window.update()  # Update the window
        
        time.sleep(1)  # Sleep for 1 second
        t -= 1
    
    # Check if notification is enabled
    if check.get():
            winsound.Beep(440, 1000)  # Beep sound

    # Display "Time's Up" message
    Label(window, 
          text="Time's Up", 
          font=('bold', 20),
          bg=bg_color,
          foreground='red').place(x=250, y=440)
    
    # Display notification on desktop
    toast = ToastNotifier()
    toast.show_toast("Notification", 
                     "Timer is Off", 
                     duration=30, 
                     icon_path=None, 
                     threaded=True)

# Create main window
window = Tk()
window.geometry('600x600')  # Set window size
window.title('Countdown Clock & Timer')  # Set window title
window.config(bg=bg_color)


# Main label
Label(window, 
      text="Countdown Clock and Timer",
      font=('Calibri',20 ,'bold'),
      bg=bg_color,
      fg=fg_color).pack(pady=20)

# Display current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
Label(window, 
      text=current_time,
      bg=bg_color,
      fg=fg_color).pack()

# Define variables for user input
check = tk.BooleanVar()
hour = tk.IntVar()
minus = tk.IntVar()
secon = tk.IntVar()

# User input for time
Label(window, 
      text="Enter time in HH:MM:SS", 
      font=('bold'),
      bg=bg_color,
      fg=fg_color).pack()

Label(window,
      text="Enter the hours",
      bg=bg_color,
      fg=fg_color).pack()
Entry(window,
      textvariable=hour, 
      width=30,
      bg=bg_color,
      fg=fg_color).pack()

Label(window,
      text="Enter the minutes",
      bg=bg_color,
      fg=fg_color).pack()
Entry(window, 
      textvariable=minus, 
      width=30,
      bg=bg_color,
      fg=fg_color).pack()

Label(window,
      text="Enter the Seconds",
      bg=bg_color,
      fg=fg_color).pack()
Entry(window, 
      textvariable=secon, 
      width=30,
      bg=bg_color,
      fg=fg_color).pack()

# Checkbox for enabling notification
Checkbutton(window,
            text='Check for Music', 
            onvalue=True, 
            variable=check,
            bg=bg_color,
            fg=fg_color).pack()



# Button to initiate countdown
Button(window, 
       text="Set Countdown", 
       command=countdown, 
       bg=btn_color).pack()

# Label to display countdown timer
timer_label = Label(window, bg=bg_color, fg=fg_color)
timer_label.pack()

# Update window and run main loop
window.mainloop()
