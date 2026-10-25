import sys
import pygame
from config import ANCHO, ALTO, FPS
from nave import Nave
from municiones import MunicionBasica, MunicionParabolica, MunicionConica
from oleadas import GestorOleadas
from colisiones import hay_colision_rectangular, resolver_choque_entre_enemigos
from hud import HUD

CADENCIA_BASICA = 10
INVULNERABILIDAD = 45
DURACION_ANUNCIO = 90


def caja(entidad):
    if hasattr(entidad, "ancho"):
        return entidad.x, entidad.y, entidad.ancho, entidad.alto
    return entidad.rect.x, entidad.rect.y, entidad.rect.width, entidad.rect.height


def nueva_partida():
    nave = Nave(ANCHO // 2 - 10, ALTO - 120)
    gestor_oleadas = GestorOleadas()
    numero_oleada = 1
    enemigos = gestor_oleadas.crear_oleada(numero_oleada)
    municiones = []
    return nave, gestor_oleadas, numero_oleada, enemigos, municiones


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Batalla Naval - MATE1133")
    reloj = pygame.time.Clock()
    hud = HUD()

    fondo_mar = pygame.image.load("img/fondo_mar.png").convert()
    fondo_mar = pygame.transform.scale(fondo_mar, (ANCHO, ALTO))
    y_fondo = 0

    nave, gestor_oleadas, numero_oleada, enemigos, municiones = nueva_partida()
    estado = "jugando"
    cooldown_basica = 0
    invulnerable = 0
    anuncio = DURACION_ANUNCIO

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif estado != "jugando" and evento.key == pygame.K_r:
                    nave, gestor_oleadas, numero_oleada, enemigos, municiones = nueva_partida()
                    estado = "jugando"
                    cooldown_basica = 0
                    invulnerable = 0
                    anuncio = DURACION_ANUNCIO
                elif estado == "jugando":
                    if evento.key in (pygame.K_2, pygame.K_x):
                        if nave.puede_disparar_parabolica():
                            municiones.append(MunicionParabolica(nave.rect.centerx, nave.rect.top))
                    elif evento.key in (pygame.K_3, pygame.K_c):
                        if nave.puede_disparar_conica():
                            municiones.append(MunicionConica(nave.rect.centerx, nave.rect.top))

        if estado == "jugando":
            y_fondo = (y_fondo + 2) % ALTO
            cooldown_basica = max(0, cooldown_basica - 1)
            invulnerable = max(0, invulnerable - 1)
            anuncio = max(0, anuncio - 1)

            teclas = pygame.key.get_pressed()
            nave.mover(teclas, ANCHO, ALTO)

            disparo_basico = teclas[pygame.K_SPACE] or teclas[pygame.K_1] or teclas[pygame.K_z]
            if disparo_basico and cooldown_basica == 0:
                municiones.append(MunicionBasica(nave.rect.centerx, nave.rect.top))
                cooldown_basica = CADENCIA_BASICA

            for proyectil in municiones:
                proyectil.actualizar()

            for enemigo in enemigos:
                enemigo.actualizar()

            resolver_choque_entre_enemigos(enemigos)

            for proyectil in municiones:
                px, py, pw, ph = caja(proyectil)
                for enemigo in enemigos:
                    ex, ey, ew, eh = caja(enemigo)
                    if enemigo.vida > 0 and hay_colision_rectangular(px, py, pw, ph, ex, ey, ew, eh):
                        enemigo.recibir_impacto(proyectil.tipo)
                        proyectil.activa = False
                        break

            municiones = [
                p for p in municiones
                if p.activa and -80 < p.x < ANCHO + 80 and -80 < p.y < ALTO + 80
            ]
            enemigos = [e for e in enemigos if e.vida > 0]

            if invulnerable == 0:
                nx, ny, nw, nh = caja(nave)
                for enemigo in enemigos:
                    ex, ey, ew, eh = caja(enemigo)
                    if hay_colision_rectangular(nx, ny, nw, nh, ex, ey, ew, eh):
                        nave.recibir_dano(enemigo.dano_a_nave)
                        invulnerable = INVULNERABILIDAD
                        break

            if nave.vida <= 0:
                estado = "game_over"
            elif len(enemigos) == 0:
                if gestor_oleadas.hay_siguiente():
                    numero_oleada += 1
                    enemigos = gestor_oleadas.crear_oleada(numero_oleada)
                    anuncio = DURACION_ANUNCIO
                else:
                    estado = "victoria"

        pantalla.blit(fondo_mar, (0, y_fondo))
        pantalla.blit(fondo_mar, (0, y_fondo - ALTO))

        for proyectil in municiones:
            proyectil.dibujar(pantalla)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        if invulnerable % 10 < 5:
            nave.dibujar(pantalla)

        hud.dibujar(pantalla, nave, numero_oleada)

        if estado == "jugando" and anuncio > 0:
            hud.dibujar_anuncio(pantalla, numero_oleada)
        elif estado == "game_over":
            hud.dibujar_game_over(pantalla)
        elif estado == "victoria":
            hud.dibujar_victoria(pantalla)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
