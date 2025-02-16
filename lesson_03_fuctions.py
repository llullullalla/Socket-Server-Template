import turtle as t
import colorama as cr


# functions are defined with the keyword 'def'
# they can have 0 to inf arguments in parentheses
# they can return values specified after the keyword 'def'
# if there is no return from function it returns 'None'
def print_hello_world(text):
    message = "Hello world: " + text
    print(cr.Fore.RED + message)
    print(cr.Style.RESET_ALL)
    return message, text


def add_two_numbers(nr1, nr2):
    result = nr1 + nr2
    return result


output = print_hello_world("everyone")
print(add_two_numbers(10, 89))


def go_forward_100():
    t.forward(100)


def make_triangle():
    for _ in range(3):
        go_forward_100()
        t.left(120)


decrement = 0.9


# this function is special because it recursively calls itself
def make_triangle_recursive(length, depth):
    # exit the function if depth is equal to 0
    if depth == 0:
        return
    # make triangle
    for _ in range(3):
        t.forward(length)
        t.left(120)
    # go to the beginning of the next triangle
    t.penup()
    t.forward((length - length * decrement) / 3)
    t.left(60)
    t.forward((length - length * decrement) / 3)
    t.right(60)
    t.pendown()
    # change argument values
    length *= decrement
    depth -= 1
    # call itself again
    return make_triangle_recursive(length, depth)


triangle_side_length = 500
t.speed(0)
t.penup()
t.goto((-triangle_side_length * 0.5, -triangle_side_length * 0.33))
t.pendown()
make_triangle_recursive(triangle_side_length, 25)

# bind function to keypress in turtle mode
t.onkey(make_triangle, "w")
t.onkey(go_forward_100, "s")
t.listen()

t.exitonclick()
