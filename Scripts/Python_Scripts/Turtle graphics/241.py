from turtle import Screen, Turtle
from colorsys import hsv_to_rgb

def draw_pattern(turtle):
    h = 0
    turtle.goto(120, -30)
    for _ in range(8):
        turtle.color(hsv_to_rgb(h, 1, 1))
        for _ in range(75):
            h += 0.0115
            turtle.forward(90)
            turtle.backward(90)
            turtle.right(3)
        turtle.forward(100)

def main():
    screen = Screen()
    screen.bgcolor("black")

    turtle = Turtle()
    turtle.speed(0)

    draw_pattern(turtle)

    screen.mainloop()

if __name__ == "__main__":
    main()
