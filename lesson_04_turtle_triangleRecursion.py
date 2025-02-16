from turtle import *
import math 

step = int(input("Draw triangle recursion number: "))
size = 400

# Renaming 'min' to avoid conflict with the built-in min function
min_size = size / (2 ** step) if step > 1 else size / 2 

pf = math.sqrt(3) / 2  # Height ratio for an equilateral triangle

def D(l, x, y):
    if l > min_size:  # Check if the length is larger than the minimum size
        l = l / 2  # Halve the length for the recursive steps
        D(l, x, y)
        D(l, x + l, y)
        D(l, x + l / 2, y + l * pf)
    else:
        goto(x, y)
        pendown()
        for _ in range(3):  # Draw an equilateral triangle
            forward(l)
            left(120)
        setheading(0)
        penup()
        goto(x, y)

penup()
speed('fastest')
D(size, -size / 2, -size * pf / 2.0)
goto(0, 0)
done()
