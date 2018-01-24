import turtle

def draw_square(some_turtle):
    for i in range(1,5):
        some_turtle.forward(100)
        some_turtle.right(90)

def draw_art():
    window = turtle.Screen()
    window.bgcolor("black")

    bob = turtle.Turtle()
    bob.shape("circle")
    bob.color("white")
    bob.speed(8)

    for i in range(1,73):
        draw_square(bob)
        bob.right(5)

    window.exitonclick()

draw_art()