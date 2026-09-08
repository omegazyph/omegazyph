########################################################################################
# Date:         2026-09-07
# Script Name:  solar_system.py
# Author:       Wayne Stock
# Updated:      2026-09-07
# Description:  A Tkinter animation displaying a solar system with orbiting planets.
########################################################################################

import math
import random
import tkinter as tk

root = tk.Tk()
root.title("SOLAR SYSTEM")
root.geometry("800x700")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=800,
    height=700,
    bg="#050018",
    highlightthickness=0
)

canvas.pack()

cx, cy = 400, 350
angle = 0

stars = []
for _ in range(100):
    stars.append((
        random.randint(0, 800),
        random.randint(0, 700),
        random.randint(1, 3)
    ))


def animate():
    global angle

    canvas.delete("all")

    # Draw stars
    for x, y, size in stars:
        canvas.create_oval(
            x, y, x + size, y + size,
            fill="white",
            outline=""
        )

    # Draw sun glow effect
    for size in range(100, 50, -10):
        canvas.create_oval(
            cx - size, cy - size,
            cx + size, cy + size,
            fill="#332000",
            outline=""
        )

    # Draw core sun
    canvas.create_oval(
        cx - 45, cy - 45,
        cx + 45, cy + 45,
        fill="#FFD700",
        outline="#FFA500",
        width=4
    )

    planets = [
        (90, "gray", 8, 4),
        (140, "orange", 12, 3),
        (200, "cyan", 14, 2),
        (260, "red", 12, 1.5),
    ]

    for orbit, color, size, speed in planets:
        # Draw orbit line
        canvas.create_oval(
            cx - orbit, cy - orbit,
            cx + orbit, cy + orbit,
            outline="#303050"
        )

        # Calculate planet positions based on current angle and speed multiplier
        a = angle * speed

        x = cx + orbit * math.cos(math.radians(a))
        y = cy + orbit * math.sin(math.radians(a))

        # Draw planet shadow/glow
        canvas.create_oval(
            x - size - 4, y - size - 4,
            x + size + 4, y + size + 4,
            fill="#202040",
            outline=""
        )

        # Draw main planet body
        canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=color,
            outline="white"
        )

    # Increment angle for rotation animation
    angle += 2

    # Call animate function after 30 milliseconds to maintain animation loop
    root.after(30, animate)


# Start the initial animation loop
animate()

root.mainloop()