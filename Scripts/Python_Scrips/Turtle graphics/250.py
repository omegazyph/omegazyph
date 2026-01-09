from turtle import *

# Set mode to 'Logo' for consistent angles
mode('logo')

# Set background color
bgcolor("black")


# Lift pen up and move to starting position
penup()
goto(-200, -150)
pendown()

# Hide the turtle icon
hideturtle()

# Set initial distance
dist = 300

# Loop to draw the design
i = 0
while i < 120:
    # Increase speed to draw faster
    speed(0)
    
    # Loop through colors
    for c in ('lime', 'red', 'deepskyblue'):  
        # Turn right by 0 degrees (redundant statement)
        right(0)
        
        # Move forward
        forward(i * 10 - 20)
        
        # Turn left by 59 degrees
        left(59)
        
        # Set pen width
        width(4)
        
        # Set pen color
        color(c)
        
        # Draw a circle
        circle(3)

    # Increment the loop variable
    i += 1

# Finish drawing
done()
