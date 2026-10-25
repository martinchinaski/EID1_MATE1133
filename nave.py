import pygame as py

class Nave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.vida = 100
        self.imagen = py.image.load("img/sprite_nave.png")
        self.imagen = self.imagen.subsurface(self.imagen.get_bounding_rect())
        alto = 110
        ancho = int(self.imagen.get_width() * alto / self.imagen.get_height())
        self.imagen = py.transform.scale(self.imagen, (ancho, alto))
        self.rect = self.imagen.get_rect()
        self.rect.x = self.x
        self.rect.y =self.y
        self.municion_parabola_restante = 10
        self.municion_canonica_restante = 5

    def mover(self, teclas, limite_ancho, limite_alto):
        if teclas[py.K_UP] and self.y > 0:
            self.y -= self.velocidad
        if teclas[py.K_DOWN] and self.y < limite_alto - self.rect.height:
            self.y += self.velocidad
        if teclas[py.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[py.K_RIGHT] and self.x < limite_ancho - self.rect.width:
            self.x += self.velocidad

        self.rect.x = self.x
        self.rect.y = self.y

    def puede_disparar_parabolica(self):
        if self.municion_parabola_restante > 0:
            self.municion_parabola_restante -= 1
            return True
        return False

    def puede_disparar_conica(self):
        if self.municion_canonica_restante > 0:
            self.municion_canonica_restante -= 1
            return True
        return False


    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0
        

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.rect.x, self.rect.y))
