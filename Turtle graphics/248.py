#2024-07-08
import turtle
screen = turtle.Screen()
screen.title("Ball Bouncing Simulation")
screen.setup(width=600,height=400)

ball= turtle.Turtle()
ball.shape("circle")
ball.color("Red")
ball.penup()
ball.speed(0)
velocity = 0
gravity = -0.2

def update():
    global velocity
    new_y = ball.ycor() + velocity
    velocity += gravity
    if new_y < -190:
        velocity *= -0.9
        new_y = -190
    ball.goto(ball.xcor(),new_y)
    screen.update()
    screen.ontimer(update,10)



update()
screen.mainloop()