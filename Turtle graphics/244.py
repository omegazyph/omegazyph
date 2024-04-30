import turtle as t
import colorsys as cs

# Set background color to black
t.bgcolor('black')

# Set the animation speed
t.tracer(50)

# Set the turtle shape and size
t.shape('turtle')
t.shapesize(5)

# Initialize hue value
h = 0

# Lift the pen up
t.up()

# Put the pen down
t.down()

# Loop to draw the design
for i in range(329):
    # Convert HSV color to RGB color
    c = cs.hsv_to_rgb(h, 1, 1)
    h += 0.008  # Increment hue value for next color

    # Draw black circle
    t.pencolor('black')
    t.circle(i, 100)
    t.rt(91)

    # Fill the shape with the generated color
    t.fillcolor(c)
    t.begin_fill()
    t.circle(i / 2, 90)
    t.end_fill()

    t.rt(91)
    t.circle(60, 90)

# Finish drawing
t.done()
