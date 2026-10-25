import math
import pygame
from config import ANCHO, ALTO, DANO_A_NAVE, DANO_MUNICION, COLOR_ROJO, COLOR_VERDE

LIMITE_SUPERIOR = 60


def cargar_sprite(ruta, ancho_max, alto_max):
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        recorte = imagen.get_bounding_rect()
        imagen = imagen.subsurface(recorte).copy()
        escala = min(ancho_max / recorte.width, alto_max / recorte.height)
        nuevo_ancho = int(recorte.width * escala)
        nuevo_alto = int(recorte.height * escala)
        return pygame.transform.smoothscale(imagen, (nuevo_ancho, nuevo_alto))
    except (pygame.error, FileNotFoundError, ValueError, ZeroDivisionError):
        return None


class Enemigo:
    def __init__(self, x, A, B, C, D, vx, vida, dano, ruta, ancho_max, alto_max, color):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.x = x
        self.vx = vx
        self.vida_max = vida
        self.vida = vida
        self.dano_a_nave = dano
        self.color = color
        self.imagen = cargar_sprite(ruta, ancho_max, alto_max)
        if self.imagen is not None:
            self.ancho, self.alto = self.imagen.get_size()
        else:
            self.ancho, self.alto = ancho_max, alto_max
        self.y = self.calcular_y()

    def calcular_y(self):
        return self.A * math.sin(self.B * self.x + self.C) + self.D

    def actualizar(self):
        self.x += self.vx
        if self.x <= 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x >= ANCHO - self.ancho:
            self.x = ANCHO - self.ancho
            self.vx = -abs(self.vx)

        d_minimo = LIMITE_SUPERIOR + self.A
        d_maximo = ALTO - self.alto - self.A
        self.D = max(d_minimo, min(d_maximo, self.D))

        self.y = self.calcular_y()

    def recibir_impacto(self, tipo_municion):
        self.vida -= DANO_MUNICION[tipo_municion]
        if self.vida < 0:
            self.vida = 0

    def dibujar_figura(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

    def dibujar(self, pantalla):
        if self.imagen is not None:
            pantalla.blit(self.imagen, (self.x, self.y))
        else:
            self.dibujar_figura(pantalla)

        proporcion = self.vida / self.vida_max
        pygame.draw.rect(pantalla, COLOR_ROJO, (self.x, self.y - 8, self.ancho, 5))
        pygame.draw.rect(pantalla, COLOR_VERDE, (self.x, self.y - 8, self.ancho * proporcion, 5))


class Enemigo1(Enemigo):
    def __init__(self, x):
        super().__init__(
            x,
            A=35, B=0.025, C=0, D=150,
            vx=2,
            vida=3,
            dano=DANO_A_NAVE["enemigo_1"],
            ruta="img/sprite_enemigo1.png",
            ancho_max=60, alto_max=100,
            color=(200, 70, 50),
        )

    def dibujar_figura(self, pantalla):
        puntos = [
            (self.x, self.y),
            (self.x + self.ancho, self.y),
            (self.x + self.ancho / 2, self.y + self.alto),
        ]
        pygame.draw.polygon(pantalla, self.color, puntos)


class Enemigo2(Enemigo):
    def __init__(self, x):
        super().__init__(
            x,
            A=55, B=0.015, C=math.pi / 2, D=260,
            vx=2.5,
            vida=6,
            dano=DANO_A_NAVE["enemigo_2"],
            ruta="img/sprite_enemigo2.png",
            ancho_max=60, alto_max=130,
            color=(70, 90, 40),
        )

    def dibujar_figura(self, pantalla):
        pygame.draw.ellipse(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))


class Enemigo3(Enemigo):
    def __init__(self, x):
        super().__init__(
            x,
            A=90, B=0.01, C=math.pi, D=330,
            vx=3,
            vida=10,
            dano=DANO_A_NAVE["enemigo_3"],
            ruta="img/sprite_enemigo3.png",
            ancho_max=110, alto_max=120,
            color=(220, 120, 30),
        )

    def dibujar_figura(self, pantalla):
        casco = self.ancho // 4
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, casco, self.alto))
        pygame.draw.rect(pantalla, self.color, (self.x + self.ancho - casco, self.y, casco, self.alto))
        pygame.draw.rect(pantalla, self.color, (self.x, self.y + self.alto / 3, self.ancho, self.alto / 3))


class JefeFinal(Enemigo):
    def __init__(self, x):
        super().__init__(
            x,
            A=45, B=0.02, C=math.pi / 4, D=180,
            vx=1.5,
            vida=40,
            dano=DANO_A_NAVE["jefe"],
            ruta="img/sprite_jefe.png",
            ancho_max=260, alto_max=260,
            color=(140, 20, 30),
        )

    def dibujar_figura(self, pantalla):
        puntos = [
            (self.x + self.ancho * 0.2, self.y),
            (self.x + self.ancho * 0.8, self.y),
            (self.x + self.ancho, self.y + self.alto * 0.5),
            (self.x + self.ancho / 2, self.y + self.alto),
            (self.x, self.y + self.alto * 0.5),
        ]
        pygame.draw.polygon(pantalla, self.color, puntos)
