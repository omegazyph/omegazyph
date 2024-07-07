from turtle  import *
from colorsys import *
bgcolor("black")

speed(0)
h=0
goto(120, -30)

for x in range(8):
    color(hsv_to_rgb(h,1,1))
    for j in range(75):
        h+0.0115
        forward(90)
        backward(90)
        right(3)

    forward(250)

done()
