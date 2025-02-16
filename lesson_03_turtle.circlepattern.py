from turtle import *

bgcolor("black")
speed(0)
penup()
goto(-200,0)
pendown()

for i in range(3):
    for colours in ["red","magenta","blue","cyan","green","yellow","white"]:
        color(colours)
        pensize(3)
        circle(150)
        forward(20)

hideturtle()
exitonclick()
