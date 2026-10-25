from enemigos import Enemigo1, Enemigo2, Enemigo3, JefeFinal


class GestorOleadas:
    def __init__(self):
        self.oleada_actual = 0
        self.total_oleadas = 4

    def crear_oleada(self, numero):
        self.oleada_actual = numero

        if numero == 1:
            return [Enemigo1(x) for x in (40, 210, 380, 550, 720)]

        if numero == 2:
            return (
                [Enemigo1(x) for x in (40, 330, 620)]
                + [Enemigo2(x) for x in (180, 470, 760)]
            )

        if numero == 3:
            return (
                [Enemigo1(x) for x in (40, 420, 780)]
                + [Enemigo2(x) for x in (230, 620)]
                + [Enemigo3(x) for x in (60, 650)]
            )

        if numero == 4:
            return (
                [JefeFinal(320)]
                + [Enemigo1(x) for x in (30, 800)]
                + [Enemigo2(x) for x in (120, 720)]
            )

        return []

    def hay_siguiente(self):
        return self.oleada_actual < self.total_oleadas
