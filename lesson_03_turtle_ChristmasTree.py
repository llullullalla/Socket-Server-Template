import turtle
import random

def draw_triangle(color, x, y, size):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(3):
        turtle.forward(size)
        turtle.left(120)
    turtle.end_fill()

def draw_rectangle(color, x, y, width, height):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
    turtle.end_fill()

def draw_circle(color, x, y, radius):
    turtle.penup()
    turtle.goto(x, y - radius)
    turtle.pendown()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()

def draw_christmas_tree():
    turtle.speed(5)
    
    # Draw tree layers
    draw_triangle("green", -50, -50, 100)
    draw_triangle("green", -40, 0, 80)
    draw_triangle("green", -30, 40, 60)
    
    # Draw tree trunk
    draw_rectangle("brown", -15, -90, 30, 40)
    
    # Draw star
    turtle.penup()
    turtle.goto(-10, 90)
    turtle.pendown()
    turtle.color("yellow")
    turtle.begin_fill()
    for _ in range(5):
        turtle.forward(20)
        turtle.right(144)
    turtle.end_fill()
    
    # Draw ornaments
    colors = ["red", "blue", "gold", "pink", "purple"]
    positions = [(-30, -20), (0, -10), (30, -20), (-20, 20), (10, 30), (20, 10)]
    for pos in positions:
        draw_circle(random.choice(colors), pos[0], pos[1], 5)
    
    turtle.hideturtle()
    turtle.done()

# Run the function
draw_christmas_tree()
