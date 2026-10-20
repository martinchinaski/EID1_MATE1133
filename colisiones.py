import math


def hay_colision_rectangular(x1, y1, ancho1, alto1, x2, y2, ancho2, alto2):
    colision_x = (x1 < x2 + ancho2) and (x1 + ancho1 > x2)
    colision_y = (y1 < y2 + alto2) and (y1 + alto1 > y2)
    return colision_x and colision_y


def hay_colision_circular(x1, y1, r1, x2, y2, r2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia <= (r1 + r2)


def _obtener_dimensiones(entidad):
    if hasattr(entidad, "ancho") and hasattr(entidad, "alto"):
        return entidad.ancho, entidad.alto
    if hasattr(entidad, "radio"):
        diametro = entidad.radio * 2
        return diametro, diametro
    if hasattr(entidad, "rect"):
        return entidad.rect.width, entidad.rect.height
    return 40, 40


def _invertir_direccion_horizontal(enemigo):
    for atributo in ("vx", "velocidad_x", "direccion", "dir_x"):
        if hasattr(enemigo, atributo):
            setattr(enemigo, atributo, -getattr(enemigo, atributo))
            return
    if hasattr(enemigo, "velocidad") and isinstance(enemigo.velocidad, (int, float)):
        enemigo.velocidad = -enemigo.velocidad


def _desplazar_eje_vertical(enemigo, delta_y):
    for atributo in ("D", "d", "y_base", "eje_y", "y_inicial"):
        if hasattr(enemigo, atributo):
            setattr(enemigo, atributo, getattr(enemigo, atributo) + delta_y)


def resolver_choque_entre_enemigos(enemigos):
    cantidad = len(enemigos)
    for i in range(cantidad):
        for j in range(i + 1, cantidad):
            e1 = enemigos[i]
            e2 = enemigos[j]

            w1, h1 = _obtener_dimensiones(e1)
            w2, h2 = _obtener_dimensiones(e2)

            if hay_colision_rectangular(e1.x, e1.y, w1, h1, e2.x, e2.y, w2, h2):
                cx1 = e1.x + w1 / 2
                cy1 = e1.y + h1 / 2
                cx2 = e2.x + w2 / 2
                cy2 = e2.y + h2 / 2

                dx = cx2 - cx1
                dy = cy2 - cy1

                solapamiento_x = (w1 + w2) / 2 - abs(dx)
                solapamiento_y = (h1 + h2) / 2 - abs(dy)

                if solapamiento_x <= solapamiento_y:
                    separacion = solapamiento_x / 2 + 1
                    if dx >= 0:
                        e1.x -= separacion
                        e2.x += separacion
                    else:
                        e1.x += separacion
                        e2.x -= separacion
                    _invertir_direccion_horizontal(e1)
                    _invertir_direccion_horizontal(e2)
                else:
                    separacion = solapamiento_y / 2 + 1
                    if dy >= 0:
                        e1.y -= separacion
                        e2.y += separacion
                        _desplazar_eje_vertical(e1, -separacion)
                        _desplazar_eje_vertical(e2, separacion)
                    else:
                        e1.y += separacion
                        e2.y -= separacion
                        _desplazar_eje_vertical(e1, separacion)
                        _desplazar_eje_vertical(e2, -separacion)

                if hasattr(e1, "rect"):
                    e1.rect.x = int(e1.x)
                    e1.rect.y = int(e1.y)
                if hasattr(e2, "rect"):
                    e2.rect.x = int(e2.x)
                    e2.rect.y = int(e2.y)


