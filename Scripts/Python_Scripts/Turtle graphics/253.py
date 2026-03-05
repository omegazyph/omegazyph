#2024-07-08
from turtle import *
import colorsys
bgcolor("black")
tracer(2)
h=0

for i in range(300):
    c=colorsys.hsv_to_rgb(h,1,1)
    color(c)
    h+=0.005
    goto(0,0)
    fd(i)
    rt(112)
    for j in range(7):
        fd(30)
        rt(143)

done()