import turtle

# Function to apply the L-system rules for a simple tree
def apply_rules(axiom):
    rules = {
        'F': 'FF',  # Rule to extend the length of the branches
        'X': 'F+[[X]-X]-F[-FX]+X'  # Rule for creating branches
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

# Function to draw an apple (a simple red circle)
def draw_apple():
    turtle.penup()
    turtle.setpos(0, 40)  # Position the apple above the tree
    turtle.pendown()
    turtle.color("red")
    turtle.begin_fill()
    turtle.circle(10)  # Draw a small circle for the apple
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
iterations = 3  # A small tree with 3 iterations
angle = 25  # Angle between branches
length = 10  # Length of each branch segment

# Draw the L-system tree
draw_l_system(axiom, iterations, angle, length)

# Draw the apple on top of the tree
draw_apple()

# Hide the turtle and display the result
turtle.hideturtle()
turtle.done()
