# garcianaranjodairo@gmail.com

import random
import sys
import pygame as pg
import tkinter as tk
from tkinter import messagebox

# Medidas
ANCHO = 600
COLUMNAS = 30

# Colores
GRIS = (40, 60, 70)
BLANCO = (255, 255, 255)
GREEN = (0, 200, 40)
RED = (255, 0, 0)
NEGRO = (0, 0, 0)


class Cubo:
    def __init__(self, start, color=RED):
        self.pos = start
        self.color = color
        self.direc_x = 1
        self.direc_y = 0

    def mover(self, direc_x, direc_y):
        self.direc_x = direc_x
        self.direc_y = direc_y
        self.pos = (self.pos[0] + self.direc_x, self.pos[1] + self.direc_y)

    def dibujar(self, screen, ojos=False):
        size_cubo = ANCHO // COLUMNAS
        x, y = self.pos
        pg.draw.rect(screen, self.color, (x * size_cubo, y * size_cubo, size_cubo, size_cubo))

        if ojos:
            centro = size_cubo // 2
            radio = 3
            circulo_medio = (x * size_cubo + centro - radio, y * size_cubo + 8)
            circulo_medio1 = (x * size_cubo + size_cubo - radio * 2, y * size_cubo + 8)
            pg.draw.circle(screen, NEGRO, circulo_medio, radio)
            pg.draw.circle(screen, NEGRO, circulo_medio1, radio)


class Snake:
    cuerpo = list()
    giros = dict()

    def __init__(self, pos, color=GREEN):
        self.color = color
        self.cabeza = Cubo(pos, color=self.color)
        self.cuerpo.append(self.cabeza)
        self.direc_x = 0
        self.direc_y = 1

    def mover(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                sys.exit()

            keys = pg.key.get_pressed()

            for _ in keys:
                if keys[pg.K_LEFT]:
                    self.direc_x = -1
                    self.direc_y = 0
                    self.giros[self.cabeza.pos[:]] = [self.direc_x, self.direc_y]
                elif keys[pg.K_RIGHT]:
                    self.direc_x = 1
                    self.direc_y = 0
                    self.giros[self.cabeza.pos[:]] = [self.direc_x, self.direc_y]
                elif keys[pg.K_UP]:
                    self.direc_x = 0
                    self.direc_y = -1
                    self.giros[self.cabeza.pos[:]] = [self.direc_x, self.direc_y]
                elif keys[pg.K_DOWN]:
                    self.direc_x = 0
                    self.direc_y = 1
                    self.giros[self.cabeza.pos[:]] = [self.direc_x, self.direc_y]
                elif keys[pg.K_ESCAPE]:
                    sys.exit()

        for i, cubo in enumerate(self.cuerpo):
            pos = cubo.pos[:]

            if pos in self.giros:
                giro = self.giros[pos]
                cubo.mover(giro[0], giro[1])
                if i == len(self.cuerpo) - 1:
                    self.giros.pop(pos)
            else:
                if cubo.direc_x == -1 and cubo.pos[0] <= 0:
                    cubo.pos = (COLUMNAS - 1, cubo.pos[1])
                elif cubo.direc_x == 1 and cubo.pos[0] >= COLUMNAS - 1:
                    cubo.pos = (0, cubo.pos[1])
                elif cubo.direc_y == 1 and cubo.pos[1] >= COLUMNAS - 1:
                    cubo.pos = (cubo.pos[0], 0)
                elif cubo.direc_y == -1 and cubo.pos[1] <= 0:
                    cubo.pos = (cubo.pos[0], COLUMNAS - 1)
                else:
                    cubo.mover(cubo.direc_x, cubo.direc_y)

    def dibujar(self, screen):
        for i, cubo in enumerate(self.cuerpo):
            if i == 0:
                cubo.dibujar(screen, True)
            else:
                cubo.dibujar(screen)

    def agregar_cubo(self):
        cola = self.cuerpo[-1]
        dx, dy = cola.direc_x, cola.direc_y

        if dx == 1 and dy == 0:
            self.cuerpo.append(Cubo((cola.pos[0] - 1, cola.pos[1]), color=color_aleatorio()))
        elif dx == -1 and dy == 0:
            self.cuerpo.append(Cubo((cola.pos[0] + 1, cola.pos[1]), color=color_aleatorio()))
        elif dx == 0 and dy == 1:
            self.cuerpo.append(Cubo((cola.pos[0], cola.pos[1] - 1), color=color_aleatorio()))
        elif dx == 0 and dy == -1:
            self.cuerpo.append(Cubo((cola.pos[0], cola.pos[1] + 1), color=color_aleatorio()))

        self.cuerpo[-1].direc_x = dx
        self.cuerpo[-1].direc_y = dy

    def reset(self, pos):
        self.cabeza = Cubo(pos, color=GREEN)
        self.cuerpo = list()
        self.cuerpo.append(self.cabeza)
        self.giros = dict()
        self.direc_x = 1
        self.direc_y = 0


def color_aleatorio():
    return random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255)


def dibujar_tablero(screen):
    size_cubo = ANCHO // COLUMNAS
    x = y = 0
    # Dibujo del tablero
    for i in range(COLUMNAS + 1):
        pg.draw.line(screen, BLANCO, (x, 0), (x, ANCHO))
        pg.draw.line(screen, BLANCO, (0, y), (ANCHO, y))
        # Transformación de coordenadas
        x = x + size_cubo
        y = y + size_cubo


def comida_aleatoria(serpiente):
    posiciones = serpiente.cuerpo

    while True:
        x = random.randrange(COLUMNAS)
        y = random.randrange(COLUMNAS)
        if len(list(filter(lambda z: z.pos == (x, y), posiciones))) > 0:
            continue
        else:
            break

    return x, y


def update(screen, comida, serpiente):
    screen.fill(GRIS)
    # Cosas a dibujar
    serpiente.dibujar(screen)
    comida.dibujar(screen)
    dibujar_tablero(screen)
    # -->
    pg.display.update()


def mensaje(subject, contenido):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, contenido)
    try:
        root.destroy()
    except BufferError:
        pass


def main():
    pg.init()
    size = ANCHO + 2, ANCHO + 2
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Snake')

    serpiente = Snake((10, 10))
    comida = Cubo(comida_aleatoria(serpiente))

    sound = pg.mixer.Sound('bounce.wav')

    reloj = pg.time.Clock()

    while True:
        pg.time.delay(50)
        reloj.tick(10)

        serpiente.mover()
        if serpiente.cuerpo[0].pos == comida.pos:
            sound.play()
            serpiente.agregar_cubo()
            comida = Cubo(comida_aleatoria(serpiente))

        for i in range(len(serpiente.cuerpo)):
            if serpiente.cuerpo[i].pos in list(map(lambda z: z.pos, serpiente.cuerpo[i + 1:])):
                print(f"Score: {len(serpiente.cuerpo)}")
                mensaje("¡You Lost!", "Play again...")
                serpiente.reset((10, 10))
                break

        update(screen, comida, serpiente)


if __name__ == '__main__':
    main()
