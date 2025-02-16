import turtle
import random

# Function to apply the L-system rules for a simple tree
def apply_rules(axiom):
    rules = {
        'F': 'FF',  # Rule to extend the length of the branches
        'X': 'F[+X]F[-X]X'  # Rule for branching with smaller sub-branches
    }
    return ''.join(rules.get(ch, ch) for ch in axiom)

# Function to draw the L-system tree
def draw_l_system(axiom, iterations, angle, length):
    stack = []
    turtle.speed(0)  # Fastest drawing speed
    for _ in range(iterations):
        axiom = apply_rules(axiom)
    
    for char in axiom:
        if char == 'F':
            turtle.forward(length)
            # Randomly draw money (bills) at the end of branches
            if random.random() < 0.1:  # 10% chance to draw a bill
                draw_dollar_bill()
        elif char == '+':
            turtle.left(angle)
        elif char == '-':
            turtle.right(angle)
        elif char == '[':
            stack.append((turtle.pos(), turtle.heading()))  # Save position and heading
        elif char == ']':
            position, heading = stack.pop()  # Restore position and heading
            turtle.penup()
            turtle.setpos(position)
            turtle.setheading(heading)
            turtle.pendown()

# Function to draw paper dollar bills (small rectangles)
def draw_dollar_bill():
    turtle.penup()
    turtle.setpos(turtle.xcor(), turtle.ycor())  # Position the bill at the current location
    turtle.pendown()
    turtle.color("green")
    turtle.begin_fill()
    for _ in range(2):  # Draw a rectangle for the bill
        turtle.forward(10)
        turtle.left(90)
        turtle.forward(5)
        turtle.left(90)
    turtle.end_fill()

# Set up the screen and turtle
screen = turtle.Screen()
screen.bgcolor("white")
turtle.penup()
turtle.setpos(0, -100)  # Start from the base of the tree
turtle.setheading(90)  # Point the turtle upward
turtle.pendown()

# Initialize parameters for the L-system tree
axiom = 'X'  # Starting axiom
iterations = 4  # More iterations for a fuller tree
angle = 30  # Angle between branches
length = 8  # Length of each branch segment

# Draw the L-system tree
draw_l_system(axiom, iterations, angle, length)

# Hide the turtle and display the result
turtle.hideturtle()
turtle.done()
