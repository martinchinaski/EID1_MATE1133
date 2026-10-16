import sys
import pygame
from config import ANCHO, ALTO, FPS, COLOR_MAR


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Batalla Naval - MATE1133")
    reloj = pygame.time.Clock()

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        pantalla.fill(COLOR_MAR)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
