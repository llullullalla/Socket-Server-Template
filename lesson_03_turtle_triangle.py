from turtle import *

speed(0)
bgcolor("blue")

penup()
goto(-150, -100)
fillcolor("yellow")
begin_fill()
pendown()

for i in range(3):
    forward(300)
    left(120)
end_fill()

hideturtle()
exitonclick()
