# some more practical examples of the OOP

import turtle


# 'subclassing' a Turtle class
class PrettyTurtle(turtle.Turtle):
    def __init__(self, visible=True):
        # IMPORTANT: unless you have a very good reason you should initialize
        # the parent class first.
        super().__init__("classic", 1000, visible)
        self.color("blue")  # change color to blue in the constructor

    # override the circle method to draw the circle from the center
    def circle(self, radius):
        self.penup()
        self.right(90)
        self.forward(radius)
        self.left(90)
        self.pendown()
        super().circle(radius)  # IMPORTANT: you have to call the parent method
        self.penup()
        self.left(90)
        self.forward(radius)
        self.right(90)
        self.pendown()

    def teleport(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()


pretty_turtle = PrettyTurtle()
pretty_turtle.teleport(50, 50)
pretty_turtle.speed(0)
pretty_turtle.circle(100)

standard_turtle = turtle.Turtle()
standard_turtle.speed(0)
standard_turtle.circle(25)

turtle.done()
