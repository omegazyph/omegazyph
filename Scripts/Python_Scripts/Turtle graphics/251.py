#2024-07-08

from turtle import *
import colorsys
bgcolor("black")
tracer(50)
speed(0)
h=0
for i in range(800):
    c=colorsys.hsv_to_rgb(h,1,0.8)
    h+=0.008
    fillcolor(c)
    pencolor(c)
    pensize(5)
    up()
    goto(-8.25,0)
    down()
    fd(i)
    rt(89)
    circle(15,320)
    end_fill()

done()