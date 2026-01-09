# this is a cicle in colors
# Wayne Stock
# date: 2024-04-29 


import turtle as t

# Set background color to black
t.bgcolor("black")

# Set the drawing speed to the fastest
t.speed(0)

# Set the pen size to 3
t.pensize(3)

# Loop to draw the circles
for i in range(200):
    # Loop to change colors after drawing each circle
    for color in ("Deeppink","Lime","Red","Green","Yellow"):
        # Set the pen color to the current color in the loop
        t.color(color)
        # Draw a circle with radius decreasing as i increases
        t.circle(100-i)
        # Turn the turtle left by 20 degrees
        t.left(20)

# Keep the window open until it's manually closed
t.done()
