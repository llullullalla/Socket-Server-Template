import turtle


def handle_onclick(x, y):
    # Write the coordinates to a file in G-code format
    with open("clicked.txt", "a") as f:
        f.write(f"G1 X{x} Y{y}\n")
    # Move the turtle to the clicked position
    turtle.goto(x, y)
    print("Clicked at", x, y)


# Set the turtle speed to the maximum
turtle.speed(0)
# Bind the onclick event to the handle_onclick function
turtle.onscreenclick(handle_onclick)
# Listen for events
turtle.listen()

# Keep the window open
turtle.done()
