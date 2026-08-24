#################################################
# Author wayne Stock
# date 2026-08-21
# Animated Cosmic Propeller Vortex
################################################

from turtle import * 
import colorsys
import time

setup(900,900)
bgcolor("black")
speed(0)
delay(0)
hideturtle()
tracer(0,0)

for i in range(360):
    r,g,b = colorsys.hsv_to_rgb((0.5 + i * 0.0015) % 1.0, 0.9, 1.0)
    color(r,g,b)
    penup()
    forward(i *0.5)
    pendown()
    left(60)
    width(i // 150 + 1)
    circle(i * 0.3, 90)
    right(120)
    circle(1 * 0.3, 90)
    penup()
    goto(0,0)
    pendown()
    right(1)
    update()
    time.sleep(0.003)
done()

