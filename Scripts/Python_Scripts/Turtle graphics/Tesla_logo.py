from turtle import *

# Set background color
getscreen().bgcolor("red")

# Set pen color
pencolor("black")

# Set drawing speed
speed(10)

# Set pen color and penup
color("white")
penup()

# Move to starting position
goto(-160, 160)

# Start drawing
pendown()

# Draw the first petal
begin_fill()
left(18)
circle(-500, extent=40)
right(90)
forward(17)
right(89.5)
circle(500, extent=39)
right(90)
forward(17)
end_fill()

# Move to the second position
penup()
goto(-155, 133)
pendown()

# Draw the second petal
begin_fill()
right(90.5)
circle(-500, extent=38)
right(70)
left(90)
circle(-20, -70)
right(10)
circle(-300, extent=15)
right(93)
forward(280)
right(160)
forward(280)
left(80)
circle(300, extent=15)
circle(20, 70)
left(80)
circle(30, -80)
end_fill()

# Move to the third position
penup()
goto(-20, 155)
pendown()

# Set pen color and fill color
pencolor("black")
color("red")

# Draw the third petal
begin_fill()
left(30)
forward(60)
left(138)
forward(65)
end_fill()

# Finish drawing
done()
