# garcianaranjodairo@gmail.com

import turtle

# Tamaño de la ventana
ANCHO: int = 800
ALTO: int = 600

SIZE_FOND = 20

MARGEN = 20

LIM_ANCHO: int = (ANCHO - MARGEN) // 2
LIM_ALTO: int = (ALTO - MARGEN) // 2


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def update(self):
        self.score = self.score + 1


class Entidad:
    def __init__(self, color, forma, inicio, velocidad):
        self.obj = turtle.Turtle()
        self.obj.speed(0)
        self.obj.shape(forma)
        self.obj.color(color)
        self.obj.penup()
        self.obj.goto(inicio)
        self.velocidad = velocidad
        self.dx = velocidad
        self.dy = velocidad


class Ball(Entidad):

    def update(self, pen, jugador1, jugador2):
        self.obj.setx(self.obj.xcor() + self.dx)
        self.obj.sety(self.obj.ycor() + self.dy)

        if self.obj.ycor() > LIM_ALTO:
            self.obj.sety(LIM_ALTO)
            self.dy = self.dy * -1

        if self.obj.ycor() < -LIM_ALTO:
            self.obj.sety(-LIM_ALTO)
            self.dy = self.dy * -1

        if self.obj.xcor() > LIM_ANCHO:
            jugador1.update()
            pen.clear()
            pen.write(f"{jugador1.name}: {jugador1.score}  {jugador2.name}: {jugador2.score}",
                      align="center", font=("Courier", SIZE_FOND, "bold"))
            self.obj.goto(0, 0)
            self.dx = self.dx * -1

        if self.obj.xcor() < -LIM_ANCHO:
            jugador2.update()
            pen.clear()
            pen.write(f"{jugador1.name}: {jugador1.score}  {jugador2.name}: {jugador2.score}",
                      align="center", font=("Courier", SIZE_FOND, "bold"))
            self.obj.goto(0, 0)
            self.dx = self.dx * -1


class Paleta(Entidad):
    def tam_forma(self, ancho, alto):
        self.obj.shapesize(stretch_wid=ancho, stretch_len=alto)

    def move_up(self):
        self.obj.sety(self.obj.ycor() + self.velocidad)

    def move_down(self):
        self.obj.sety(self.obj.ycor() - self.velocidad)


def main():
    ventana = turtle.Screen()
    ventana.title('Pong')
    ventana.bgcolor('black')
    ventana.setup(ANCHO + 50, ALTO + 50)
    ventana.tracer(0)

    ventana.delay(10)

    ball = Ball('white', 'circle', (0, 0), 0.1)

    izq = Paleta('white', 'square', (-LIM_ANCHO, 0), 12)
    izq.tam_forma(5, 1)

    der = Paleta('white', 'square', (LIM_ANCHO, 0), 12)
    der.tam_forma(5, 1)

    jugador1 = Player("Jugador A")
    jugador2 = Player("Jugador B")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("red")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write(f"{jugador1.name}: {jugador1.score}  {jugador2.name}: {jugador2.score}",
              align="center", font=("Courier", SIZE_FOND, "bold"))

    ventana.listen()
    ventana.onkeypress(izq.move_up, 'w')
    ventana.onkeypress(izq.move_down, 's')

    ventana.onkeypress(der.move_up, 'Up')
    ventana.onkeypress(der.move_down, 'Down')

    while True:
        ventana.update()
        ball.update(pen, jugador1, jugador2)

        if ball.obj.xcor() < -LIM_ANCHO + 20 and \
                izq.obj.ycor() + 50 > ball.obj.ycor() > izq.obj.ycor() - 50:
            ball.dx = ball.dx * -1

        if ball.obj.xcor() > LIM_ANCHO - 20 and \
                der.obj.ycor() + 50 > ball.obj.ycor() > der.obj.ycor() - 50:
            ball.dx = ball.dx * -1


if __name__ == '__main__':
    main()
