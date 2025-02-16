import turtle

def draw_rectangle(t, color, x, y, width, height):
    t.penup()
    t.color(color)
    t.fillcolor(color)
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for i in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.setheading(0)

def draw_star(t, color, x, y, size):
    t.penup()
    t.color(color)
    t.fillcolor(color)
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for i in range(5):
        t.forward(size)
        t.right(144)
        t.forward(size)
    t.end_fill()
    t.setheading(0)

# Setup the screen and turtle
screen = turtle.Screen()
t = turtle.Turtle()

# Example function calls
draw_rectangle(t, 'blue', -100, 100, 200, 100)
draw_star(t, 'yellow', 0, 0, 50)

# Finish the drawing
turtle.done()
