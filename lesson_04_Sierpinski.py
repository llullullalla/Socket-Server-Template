import turtle as t

def draw_same_sided_triangle(length):
    t.pendown()
    for _ in range(3):
        t.forward(length)
        t.left(120)
    t.penup()


def draw_sierpinski(length, depth):
    if depth == 0:
        draw_same_sided_triangle(length)
    else:
        length *= 0.5
        depth -= 1
        for i in range(3):  # Use `i` here for the loop variable
            draw_sierpinski(length, depth)
            if i == 0:
                t.left(60)
                t.forward(length)
                t.right(60)
            elif i == 1:
                t.forward(length)
                t.right(120)
            else:
                t.forward(length)
                t.right(60)
                t.forward(length)
                t.right(180)


t.speed(0)
t.penup()
t.goto(-200, -100)
draw_sierpinski(400, 7)  # Corrected function name

t.exitonclick()
