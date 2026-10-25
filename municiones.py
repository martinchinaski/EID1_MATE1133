import pygame as py
import math

class MunicionBasica:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = -7
        self.activa = True
        self.tipo = "basica"
        self.imagen = py.image.load("img/sprite_municion_basica.png")
        self.imagen = self.imagen.subsurface(self.imagen.get_bounding_rect())
        self.imagen = py.transform.scale(self.imagen, (8, 22))
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class MunicionParabolica:
    def __init__(self, x, y):
        self.x_inicial = x
        self.y_inicial = y
        self.x = x
        self.y = y
        self.t = 0
        self.activa = True
        self.tipo = "parabolica"
        self.imagen = py.image.load("img/sprite_municion_parabolica.png")
        self.imagen = self.imagen.subsurface(self.imagen.get_bounding_rect())
        self.imagen = py.transform.scale(self.imagen, (12, 26))
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        self.t += 0.5
        self.x = self.x_inicial + 8 *self.t
        self.y = self.y_inicial - 2 * (self.t ** 2)
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class MunicionConica:
    def __init__(self, x, y):
        self.x_centro = x
        self.y_centro = y
        self.x = x
        self.y = y
        self.t = 0
        self.activa = True
        self.tipo = "conica"
        self.imagen = py.image.load("img/sprite_municion_canonica.png")
        self.imagen = self.imagen.subsurface(self.imagen.get_bounding_rect())
        self.imagen = py.transform.scale(self.imagen, (16, 34))
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        self.t += 0.2
        self.y_centro -= 5
        self.x = self.x_centro + 60 * math.cos(self.t)
        self.y = self.y_centro + 25 * math.sin(self.t)
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
