#2024-07-07
import turtle
import random


#set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create a turtle
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Define colors
colors = ["white", "yellow", "cyan", "orange", "pink"]

# Draw stars
def draw_star(x, y, size):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(random.choice(colors))
    for x in range(5):
        pen.forward(size)
        pen.right(144)

# Draw sheeting stars
def draw_sheeting_star(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color("white")
    pen.forward(30)
    pen.right(135)
    pen.forward(30)
    pen.left(136)
    pen.forward(30)

# Draw the starry night shy
for x in range(50):
    x = random.randint(-300, 300)
    y = random.randint(-200, 200)
    size = random.randint(5, 20)
    draw_star(x, y, size)

# Draw shooting stars
for x in range(10):
    x = random.randint(-300, 300)
    y = random.randint(-100, 100)
    draw_star(x, y, size)

# Hide the turtle
pen.hideturtle()

# Keep the window open
turtle.done()
