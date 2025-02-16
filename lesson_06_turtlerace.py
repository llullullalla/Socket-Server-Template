import time
import turtle
import random

BOUNDS = 500
MAX_PUDDLE_RADIUS = 50
MIN_PUDDLE_RADIUS = 10
PUDDLE_COLOR = (0.6, 0.6, 1)


def circle_from_middle(radius):
    """
    Make a circle around the current turtle position.
    """
    turtle.penup()
    turtle.right(90)
    turtle.forward(radius)
    turtle.left(90)
    turtle.pendown()
    turtle.circle(radius)
    turtle.penup()
    turtle.left(90)
    turtle.forward(radius)
    turtle.right(90)
    turtle.pendown()


def teleport(trt, x, y):
    """
    Go to x,y without making a line.
    """
    trt.penup()
    trt.goto(x, y)


# standard vector distance calculation
def calculate_distance(vec1, vec2):
    ret = ((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) ** 2) ** 0.5
    return ret


# make a Puddle class that will remember its position and radius
class Puddle:
    def __init__(self):
        turtle.speed(0)
        turtle.hideturtle()
        self.pos_x = random.random() * BOUNDS - BOUNDS * 0.5
        self.pos_y = random.random() * BOUNDS - BOUNDS * 0.5
        teleport(turtle, self.pos_x, self.pos_y)
        turtle.pendown()
        turtle.color(PUDDLE_COLOR)
        turtle.fillcolor(PUDDLE_COLOR)
        self.radius = (
            random.random() * (MAX_PUDDLE_RADIUS - MIN_PUDDLE_RADIUS)
            + MIN_PUDDLE_RADIUS
        )
        turtle.begin_fill()
        circle_from_middle(self.radius)
        turtle.end_fill()

    def get_pos(self):
        return (self.pos_x, self.pos_y)


class Car:
    def __init__(self, name, pos_x, pos_y, speed, puddle_speed):
        self.name = name
        self._speed = speed
        self._puddle_speed = puddle_speed

        self._turtle = turtle.Turtle(shape="turtle", visible=False)
        self._turtle.speed(5)
        self._turtle.color((random.random(), random.random(), random.random()))
        self.is_in_puddle = False
        teleport(self._turtle, pos_x, pos_y)
        self._turtle.showturtle()

    # go forward. The speed is chosen based on the _is_in_puddle
    def forward(self):
        self._turtle.pendown()
        if self._is_in_puddle:
            self._turtle.forward(self._puddle_speed)
        else:
            self._turtle.forward(self._speed)

    def get_pos(self):
        return self._turtle.pos()

    # check if the car is in a puddle
    def check_for_puddles(self, puddles):
        self._is_in_puddle = False
        # iterate over the puddle list
        for p in puddles:
            d = calculate_distance(self.get_pos(), p.get_pos())
            # if the disatnce to the puddle center is less than
            # the radius of the puddle the car is in the puddle
            if d < p.radius:
                self._is_in_puddle = True
                break


class ToyotaTundra(Car):
    def __init__(self, name, pos_x, pos_y):
        super().__init__(name, pos_x, pos_y, 3, 7)


class Porsche911(Car):
    def __init__(self, name, pos_x, pos_y):
        super().__init__(name, pos_x, pos_y, 9, 2)


def run_game():
    puddles = []
    # make some puddles
    for _ in range(25):
        puddles.append(Puddle())

    # make some cars
    cars = [
        Porsche911("Porche0", -250, -75),
        Porsche911("Porche1", -250, -25),
        ToyotaTundra("Toyota0", -250, 25),
        ToyotaTundra("Toyota1", -250, 75),
    ]
    winner = None
    # run until we have a winner
    while winner is None:
        for c in cars:
            c.check_for_puddles(puddles)
            c.forward()
            # winner condition: the X position of the car is more than 250 px
            if c.get_pos()[0] > 250:
                winner = c
                break
        time.sleep(0.05)
    if winner:
        print(f"{winner.name} wins!")
    else:
        print("Nobody won!")
    turtle.done()


run_game()
