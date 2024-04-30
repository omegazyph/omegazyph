import turtle as t

t.bgcolor("black")
t.speed(0)
t.pensize(3)

for i in range(200):
    for color in ("Deeppink","Lime","Red"):
        t.color(color)
        t.circle(100-i)
        t.left(20)

t.draw()
t.done()