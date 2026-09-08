################################################
# date: 2026-09-07
# Script Name: smart.py
# Author: Wayne Stock
# updated: 2026-09-07
# Discription:
#################################################

import turtle

t = turtle.Turtle()
t.pensize(4)

colors = ["blue","black","red","yellow","green"]
positions = [(-120, 0), (0, 0), (120, 0), (-60, -50), (60, -50)]

for color, pos in zip(colors, positions):
    t.penup()
    t.goto(pos)
    t.pendown()
    t.color(color)
    t.circle(50)

turtle.done()