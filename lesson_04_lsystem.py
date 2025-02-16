import turtle as t


# take one character from "axiom" string one at the time and
# swap it with the character string defined in "rules" dictionary
# e.g. for a rule A->AB every A will become AB
def expand_axiom(axiom, rules):
    result = ""
    for c in axiom:
        if c in CONSTANTS:
            result += c
            continue
        if c in rules:
            result += rules[c]
    return result


# iterate over the input "axiom" and axpand it
# every iteration the "result" string grows exponentialy bigger
# and bigger
def iterate(rules, iteration_count, axiom):
    result = axiom
    for _ in range(iteration_count):
        result = expand_axiom(result, rules)
    return result


# draw with a turtle based on the input "axiom" (can be
# understood as a set of instructions) and
# a set of behaviors (specified in the if-else condition)
def draw(axiom, step, angle):
    # go to the initial position
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.goto(0, -300)
    t.pendown()
    # turn turtle pointing UP
    t.left(90)
    # initialize a "stack" that will remember past positions
    stack = []
    for i in range(len(axiom)):
        c = axiom[i]
        if c == "X":
            t.forward(step * 0.5)
        elif c == "Y":
            t.forward(step)
        elif c == "+":
            t.left(angle)
        elif c == "-":
            t.right(angle)
        elif c == "[":
            # add current position and heading  to the "stack"
            stack.append((t.heading(), t.position()))
        elif c == "]":
            # return and delete last position and heading
            heading, pos = stack.pop()
            # go to the previous position
            t.penup()
            t.goto(pos)
            # point turtle to the previous heading
            t.setheading(heading)
            t.pendown()


# constants are special characters not expanded by rules
# this datatype is a set
CONSTANTS = {"+", "-", "[", "]"}

step = 5  # a single length step (e.g. a length of the "forward" instruction)
angle = 45  # a single angle step (e.g. an angle of the "left" instruction)
axiom = "Y"  # starting "axiom" string
rules = {"X": "XX", "Y": "X[+Y]-Y"}  # rules to be applied to the "axiom" string
axiom = iterate(rules, 8, axiom)  # expand the starting "axiom" with the "rules"
print(axiom)  # print the expanded axiom
draw(axiom, step, angle)  # draw with turtle
t.exitonclick()
