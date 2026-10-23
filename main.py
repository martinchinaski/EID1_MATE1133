import sys
import pygame
from config import (
    ANCHO,
    ALTO,
    FPS,
    COLOR_MAR,
    VIDA_INICIAL_NAVE,
    DANO_A_NAVE,
)
from nave import Nave
from municiones import MunicionBasica, MunicionParabolica, MunicionConica
from oleadas import GestorOleadas
from colisiones import (
    hay_colision_rectangular,
    hay_colision_circular,
    resolver_choque_entre_enemigos,
)
from hud import HUD


def _caja_entidad(entidad, ancho_defecto=40, alto_defecto=40):
    x = getattr(entidad, "x", 0)
    y = getattr(entidad, "y", 0)
    if hasattr(entidad, "ancho") and hasattr(entidad, "alto"):
        return x, y, entidad.ancho, entidad.alto
    if hasattr(entidad, "radio"):
        r = entidad.radio
        return x - r, y - r, r * 2, r * 2
    if hasattr(entidad, "rect"):
        return entidad.rect.x, entidad.rect.y, entidad.rect.width, entidad.rect.height
    return x, y, ancho_defecto, alto_defecto


def _tipo_municion(proyectil):
    if hasattr(proyectil, "tipo"):
        return proyectil.tipo
    nombre = proyectil.__class__.__name__.lower()
    if "parabol" in nombre:
        return "parabolica"
    if "conic" in nombre or "canonic" in nombre:
        return "conica"
    return "basica"


def _dano_enemigo(enemigo):
    if hasattr(enemigo, "dano_a_nave"):
        return enemigo.dano_a_nave
    nombre = enemigo.__class__.__name__.lower()
    if "jefe" in nombre:
        return DANO_A_NAVE["jefe"]
    if "3" in nombre:
        return DANO_A_NAVE["enemigo_3"]
    if "2" in nombre:
        return DANO_A_NAVE["enemigo_2"]
    return DANO_A_NAVE["enemigo_1"]


def _impacto_proyectil_enemigo(proyectil, enemigo):
    ex, ey, ew, eh = _caja_entidad(enemigo, 40, 40)
    if hasattr(proyectil, "radio") and hasattr(enemigo, "radio"):
        return hay_colision_circular(
            proyectil.x, proyectil.y, proyectil.radio,
            enemigo.x, enemigo.y, enemigo.radio,
        )
    px, py, pw, ph = _caja_entidad(proyectil, 10, 10)
    return hay_colision_rectangular(px, py, pw, ph, ex, ey, ew, eh)


def _mover_nave(nave, teclas):
    try:
        nave.mover(teclas, ANCHO, ALTO)
    except TypeError:
        nave.mover(teclas)


def _iniciar_partida():
    nave = Nave(ANCHO // 2 - 50, ALTO - 110)
    if not hasattr(nave, "vida"):
        nave.vida = VIDA_INICIAL_NAVE
    if not hasattr(nave, "x"):
        nave.x = ANCHO // 2 - 50
    if not hasattr(nave, "y"):
        nave.y = ALTO - 110

    gestor_oleadas = GestorOleadas()
    numero_oleada = 1
    oleada_inicial = gestor_oleadas.crear_oleada(numero_oleada)
    oleadas_activas = isinstance(oleada_inicial, list)
    enemigos = oleada_inicial if oleadas_activas else []
    municiones = []
    return nave, gestor_oleadas, numero_oleada, enemigos, municiones, oleadas_activas


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Batalla Naval - MATE1133")
    reloj = pygame.time.Clock()
    hud = HUD()

    (
        nave,
        gestor_oleadas,
        numero_oleada,
        enemigos,
        municiones,
        oleadas_activas,
    ) = _iniciar_partida()

    estado = "jugando"
    cooldown_disparo_basico = 0
    cooldown_dano_nave = 0

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif estado in ("game_over", "victoria") and evento.key == pygame.K_r:
                    (
                        nave,
                        gestor_oleadas,
                        numero_oleada,
                        enemigos,
                        municiones,
                        oleadas_activas,
                    ) = _iniciar_partida()
                    estado = "jugando"
                    cooldown_disparo_basico = 0
                    cooldown_dano_nave = 0
                elif estado == "jugando":
                    nx, ny, nw, _ = _caja_entidad(nave, 40, 40)
                    cx_disparo = nx + nw // 2
                    if evento.key in (pygame.K_2, pygame.K_x):
                        puede = True
                        if hasattr(nave, "puede_disparar_parabolica"):
                            puede = nave.puede_disparar_parabolica()
                        if puede:
                            municiones.append(MunicionParabolica(cx_disparo, ny))
                    elif evento.key in (pygame.K_3, pygame.K_c):
                        puede = True
                        if hasattr(nave, "puede_disparar_conica"):
                            puede = nave.puede_disparar_conica()
                        elif hasattr(nave, "puede_disparar_canonica"):
                            puede = nave.puede_disparar_canonica()
                        if puede:
                            municiones.append(MunicionConica(cx_disparo, ny))

        if estado == "jugando":
            if cooldown_disparo_basico > 0:
                cooldown_disparo_basico -= 1
            if cooldown_dano_nave > 0:
                cooldown_dano_nave -= 1

            teclas = pygame.key.get_pressed()
            _mover_nave(nave, teclas)

            if (
                teclas[pygame.K_SPACE]
                or teclas[pygame.K_1]
                or teclas[pygame.K_z]
            ) and cooldown_disparo_basico == 0:
                nx, ny, nw, _ = _caja_entidad(nave, 40, 40)
                municiones.append(MunicionBasica(nx + nw // 2, ny))
                cooldown_disparo_basico = 12

            municiones_vivas = []
            for proyectil in municiones:
                proyectil.actualizar()
                if not getattr(proyectil, "activa", True):
                    continue
                if hasattr(proyectil, "x") and hasattr(proyectil, "y"):
                    if (
                        proyectil.x < -80
                        or proyectil.x > ANCHO + 80
                        or proyectil.y < -80
                        or proyectil.y > ALTO + 80
                    ):
                        continue
                municiones_vivas.append(proyectil)
            municiones = municiones_vivas

            for enemigo in enemigos:
                enemigo.actualizar()

            resolver_choque_entre_enemigos(enemigos)

            proyectiles_impactados = set()
            enemigos_sobrevivientes = []

            for enemigo in enemigos:
                if not hasattr(enemigo, "x") or not hasattr(enemigo, "y"):
                    enemigos_sobrevivientes.append(enemigo)
                    continue

                for idx_p, proyectil in enumerate(municiones):
                    if idx_p in proyectiles_impactados:
                        continue
                    if not hasattr(proyectil, "x") or not hasattr(proyectil, "y"):
                        continue
                    if _impacto_proyectil_enemigo(proyectil, enemigo):
                        proyectiles_impactados.add(idx_p)
                        if hasattr(proyectil, "activa"):
                            proyectil.activa = False
                        enemigo.recibir_impacto(_tipo_municion(proyectil))

                vida_enemigo = getattr(enemigo, "vida", 1)
                activo_enemigo = getattr(enemigo, "activo", True) and getattr(
                    enemigo, "vivo", True
                )
                if vida_enemigo > 0 and activo_enemigo:
                    enemigos_sobrevivientes.append(enemigo)

            enemigos = enemigos_sobrevivientes
            municiones = [
                p for i, p in enumerate(municiones) if i not in proyectiles_impactados
            ]

            if hasattr(nave, "x") and hasattr(nave, "y") and cooldown_dano_nave == 0:
                nx, ny, nw, nh = _caja_entidad(nave, 40, 40)
                for enemigo in enemigos:
                    if not hasattr(enemigo, "x") or not hasattr(enemigo, "y"):
                        continue
                    ex, ey, ew, eh = _caja_entidad(enemigo, 40, 40)
                    if hay_colision_rectangular(nx, ny, nw, nh, ex, ey, ew, eh):
                        dano = _dano_enemigo(enemigo)
                        nave.recibir_dano(dano)
                        if hasattr(nave, "vida") and nave.vida == VIDA_INICIAL_NAVE:
                            nave.vida = max(0, nave.vida - dano)
                        cooldown_dano_nave = 45
                        break

            if getattr(nave, "vida", VIDA_INICIAL_NAVE) <= 0:
                estado = "game_over"

            if oleadas_activas and len(enemigos) == 0 and estado == "jugando":
                hay_mas = gestor_oleadas.hay_siguiente()
                if hay_mas is None:
                    hay_mas = numero_oleada < 4
                if hay_mas:
                    numero_oleada += 1
                    nueva_oleada = gestor_oleadas.crear_oleada(numero_oleada)
                    enemigos = nueva_oleada if isinstance(nueva_oleada, list) else []
                else:
                    estado = "victoria"

        pantalla.fill(COLOR_MAR)

        for proyectil in municiones:
            proyectil.dibujar(pantalla)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        nave.dibujar(pantalla)
        hud.dibujar(pantalla, nave, numero_oleada)

        if estado == "game_over":
            hud.dibujar_game_over(pantalla)
        elif estado == "victoria":
            hud.dibujar_victoria(pantalla)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


