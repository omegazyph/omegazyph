import turtle as t
import colorsys as cs

t.bgcolor('black')
t.tracer(50)
t.shape('turtle')
t.shapesize(5)
h=0
t.up()
t.down()
for i in range(329):
    c=cs.hsv_to_rgb(h,1,1)
    h+=0.008
    t.pencolor('black')
    t.circle(i,100)
    t.rt(91)
    t.fillcolor(c)
    t.begin_fill()
    t.circle(i/2,90)
    t.end_fill()
    t.rt(91)
    t.circle(60,90)
t.done()
