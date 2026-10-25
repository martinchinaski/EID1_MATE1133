import pygame
from config import (
    ANCHO,
    ALTO,
    VIDA_INICIAL_NAVE,
    COLOR_BLANCO,
    COLOR_NEGRO,
    COLOR_GRIS_OSCURO,
    COLOR_VERDE,
    COLOR_AMARILLO,
    COLOR_ROJO,
    COLOR_CELESTE,
)


class HUD:
    def __init__(self):
        pygame.font.init()
        self.fuente_hud = pygame.font.SysFont("consolas", 16, bold=True)
        self.fuente_oleada = pygame.font.SysFont("consolas", 20, bold=True)
        self.fuente_titulo = pygame.font.SysFont("consolas", 56, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("consolas", 24, bold=True)

    def _color_barra_vida(self, proporcion):
        if proporcion > 0.5:
            return COLOR_VERDE
        if proporcion > 0.25:
            return COLOR_AMARILLO
        return COLOR_ROJO

    def dibujar(self, pantalla, nave, numero_oleada):
        barra_superior = pygame.Surface((ANCHO, 54), pygame.SRCALPHA)
        barra_superior.fill((10, 20, 35, 190))
        pantalla.blit(barra_superior, (0, 0))
        pygame.draw.line(pantalla, COLOR_CELESTE, (0, 54), (ANCHO, 54), 2)

        vida_actual = max(0, getattr(nave, "vida", VIDA_INICIAL_NAVE))
        vida_max = VIDA_INICIAL_NAVE
        proporcion = max(0.0, min(1.0, vida_actual / vida_max))

        x_barra = 14
        y_barra = 16
        ancho_barra = 150
        alto_barra = 22

        pygame.draw.rect(
            pantalla,
            COLOR_GRIS_OSCURO,
            (x_barra, y_barra, ancho_barra, alto_barra),
            border_radius=4,
        )
        ancho_relleno = int(ancho_barra * proporcion)
        if ancho_relleno > 0:
            pygame.draw.rect(
                pantalla,
                self._color_barra_vida(proporcion),
                (x_barra, y_barra, ancho_relleno, alto_barra),
                border_radius=4,
            )
        pygame.draw.rect(
            pantalla,
            COLOR_BLANCO,
            (x_barra, y_barra, ancho_barra, alto_barra),
            width=2,
            border_radius=4,
        )

        texto_vida = self.fuente_hud.render(
            f"VIDA {int(vida_actual)}/{vida_max}", True, COLOR_BLANCO
        )
        rect_vida = texto_vida.get_rect(midleft=(x_barra + ancho_barra + 10, 27))
        pantalla.blit(texto_vida, rect_vida)

        if numero_oleada >= 4:
            etiqueta_oleada = "JEFE FINAL"
            color_oleada = COLOR_ROJO
        else:
            etiqueta_oleada = f"OLEADA {numero_oleada}/3"
            color_oleada = COLOR_AMARILLO

        superficie_oleada = self.fuente_oleada.render(
            etiqueta_oleada, True, color_oleada
        )
        rect_oleada = superficie_oleada.get_rect(center=(420, 27))
        pantalla.blit(superficie_oleada, rect_oleada)

        parabolica = getattr(nave, "municion_parabola_restante", 10)
        conica = getattr(
            nave,
            "municion_conica_restante",
            getattr(nave, "municion_canonica_restante", 5),
        )
        texto_municiones = f"[1]Basica:INF [2]Parab:{parabolica} [3]Conica:{conica}"
        superficie_mun = self.fuente_hud.render(
            texto_municiones, True, COLOR_CELESTE
        )
        rect_mun = superficie_mun.get_rect(midright=(ANCHO - 14, 27))
        pantalla.blit(superficie_mun, rect_mun)

    def _dibujar_pantalla_final(self, pantalla, titulo, color_titulo, detalle):
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((10, 15, 25, 210))
        pantalla.blit(velo, (0, 0))

        caja_ancho = 620
        caja_alto = 220
        caja_x = (ANCHO - caja_ancho) // 2
        caja_y = (ALTO - caja_alto) // 2

        pygame.draw.rect(
            pantalla,
            COLOR_NEGRO,
            (caja_x, caja_y, caja_ancho, caja_alto),
            border_radius=10,
        )
        pygame.draw.rect(
            pantalla,
            color_titulo,
            (caja_x, caja_y, caja_ancho, caja_alto),
            width=3,
            border_radius=10,
        )

        sup_titulo = self.fuente_titulo.render(titulo, True, color_titulo)
        rect_titulo = sup_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
        pantalla.blit(sup_titulo, rect_titulo)

        sup_detalle = self.fuente_subtitulo.render(detalle, True, COLOR_BLANCO)
        rect_detalle = sup_detalle.get_rect(center=(ANCHO // 2, ALTO // 2 + 15))
        pantalla.blit(sup_detalle, rect_detalle)

        sup_controles = self.fuente_hud.render(
            "Presiona [R] para reiniciar o [ESC] para salir", True, COLOR_CELESTE
        )
        rect_controles = sup_controles.get_rect(center=(ANCHO // 2, ALTO // 2 + 65))
        pantalla.blit(sup_controles, rect_controles)

    def dibujar_anuncio(self, pantalla, numero_oleada):
        if numero_oleada >= 4:
            texto = "¡JEFE FINAL!"
            color = COLOR_ROJO
        else:
            texto = f"OLEADA {numero_oleada}"
            color = COLOR_AMARILLO
        sombra = self.fuente_titulo.render(texto, True, COLOR_NEGRO)
        superficie = self.fuente_titulo.render(texto, True, color)
        rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(sombra, (rect.x + 3, rect.y + 3))
        pantalla.blit(superficie, rect)

    def dibujar_game_over(self, pantalla):
        self._dibujar_pantalla_final(
            pantalla,
            "GAME OVER",
            COLOR_ROJO,
            "Tu nave ha sido destruida",
        )

    def dibujar_victoria(self, pantalla):
        self._dibujar_pantalla_final(
            pantalla,
            "¡VICTORIA!",
            COLOR_VERDE,
            "Has derrotado a todas las oleadas y al Jefe Final",
        )


