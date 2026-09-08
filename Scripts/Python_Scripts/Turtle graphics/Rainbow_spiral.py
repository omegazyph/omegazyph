#################################################
# Date:         2026-09-08
# Script Name:  Rainbow_spiral.py
# Autor:        wayne stock
# Updated:      2026-09-08
# discription:  using turtle to make circle
#################################################

import colorsys
import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Rainboe Sprial")
screen.setup(width=800, height=800)
t = turtle.Turtle()
t.speed(0)
t.width(2)
t.hideturtle()
h = 0
for i in range(360):
    r,g,b = colorsys.hsv_to_rgb(h,1,1)
    t.pencolor(r,g,b)
    t.circle(150)
    t.left(10)
    h = (h + 1/36) % 1

turtle.done()