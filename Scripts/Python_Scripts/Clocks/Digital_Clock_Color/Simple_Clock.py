#################################################
# Date:         2026-09-08
# Script name:  Simple_clock.py
# Author:       Wayne Stock
# updated:      2026-09-08
# Disscription: just a simple clock using tkinker
#################################################

import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("Simple Clock")

def time():
    my_time = strftime("%H:%M:%S %p")
    clock.config(text = my_time)
    clock.after(1000, time)

clock = tk.Label(root, font= ("arial", 40, "bold"),
                 background= "dark blue",
                 foreground= "white")
clock.pack(anchor="center")

time()

if __name__ == "__main__":
    root.mainloop()