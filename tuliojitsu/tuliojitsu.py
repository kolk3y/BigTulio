from PIL import Image, ImageDraw, ImageFont
from tuliojitsu.cartas import get_penguins as obtener_mazo

from tuliojitsu.parametros import RUTA_CARTAS_JUGADOR, RUTA_CARTAS_JUEGO, RUTA_BARAJAS, \
    RUTA_IMAGEN_ESPERA, RUTA_IMAGEN_JUGADAS, RUTA_IMAGEN_VICTORIA, RUTA_IMAGEN_FICHAS, DEBILIDADES

class Tuliojitsu:
    def __init__(self): #los diccionarios siguen la siguiente forma: {"1": info, "2": info)
        super().__init__()
        self.value = None #Ni idea
        self.jugadores = {} #diccionario con los nombres de los jugadores
        self.mazos = {} #diccionario con los mazos (diccionario) de los jugadores
        self.barajas = {} #diccionario con las barajas (diccionario) de los jugadores
        self.duelo = {} #diccionario que posee las cartas jugadas por cada jugador
        self.fichas = {"1": {"fuego": [], "agua": [], "nieve": []},
                       "2": {"fuego": [], "agua": [], "nieve": []}} #elemento: List(color)
        self.posiciones_ficha = {"1": {"fuego": (21, 12), "agua": (101, 12), "nieve": (181, 12)},
                                 "2": {"fuego": (920, 12), "agua": (840, 12), "nieve": (760, 12)}} #pos x de las fichas
        self.debilidades = DEBILIDADES

    def sala_espera(self, usuario):
        if len(self.jugadores) != 2:

            if len(self.jugadores) == 0:
                self.jugadores["1"] = usuario

                return ("Falta un jugador para comenzar la partida")

            elif len(self.jugadores) == 1:
                self.jugadores["2"] = usuario

                jugador_1 = self.jugadores.get("1")
                jugador_2 = self.jugadores.get("2")

                self.repartir_cartas()
                return (f"Comenzando la partida entre {jugador_1} y {jugador_2}")

        else:
            jugador_1 = self.jugadores.get("1")
            jugador_2 = self.jugadores.get("2")
            return (f"Ya hay una partida en curso entre {jugador_1} y {jugador_2}")
 
    def repartir_cartas(self): #se reparten 15 cartas al azar a cada jugador
        self.mazos["1"] = obtener_mazo()
        self.mazos["2"] = obtener_mazo()

        self.entregar_baraja()

    def entregar_baraja(self):
        cartas_j1 = Image.open(RUTA_CARTAS_JUGADOR.format("o", "1"))
        cartas_j2 = Image.open(RUTA_CARTAS_JUGADOR.format("o", "2"))

        self.posiciones = [140, 493, 846, 1199, 1552]
        baraja_j1 = {}
        baraja_j2 = {}
        for indice in range(5): #hacer función mejor
            carta_j1 = self.mazos.get("1").get(str(indice)) #se obtiene el mazo y luego la carta 'indice' del mazo
            baraja_j1[str(indice)] = carta_j1
            ruta_j1 = self.obtener_ruta(carta_j1)

            carta_j2 = self.mazos.get("2").get(str(indice))
            baraja_j2[str(indice)] = carta_j2
            ruta_j2 = self.obtener_ruta(carta_j2)

            imagen_j1 = Image.open(RUTA_CARTAS_JUEGO.format("o", ruta_j1))
            imagen_j2 = Image.open(RUTA_CARTAS_JUEGO.format("o", ruta_j2))

            cartas_j1.paste(imagen_j1, (self.posiciones[indice], 100))
            cartas_j2.paste(imagen_j2, (self.posiciones[indice], 100))

        mazos = {"1": [], "2": []}
        for indice in range(5, 15):
            mazos.get("1").append(self.mazos.get("1").get(str(indice)))
            mazos.get("2").append(self.mazos.get("2").get(str(indice)))

        self.mazos = mazos

        self.barajas["1"] = baraja_j1
        self.barajas["2"] = baraja_j2

        cartas_j1.save(RUTA_BARAJAS.format("m", "1"))
        cartas_j2.save(RUTA_BARAJAS.format("m", "2"))

    def obtener_ruta(self, carta):
        color = carta.get("color")
        elemento = carta.get("elemento")
        puntos = carta.get("puntos")

        return f"{color}_{elemento}_{puntos}"

    def manejar_duelo(self, n_jugador, indice):
        carta = self.barajas.get(n_jugador).get(indice)
        self.duelo[n_jugador] = carta

        if len(self.duelo) == 1:
            self.actualizar_baraja(n_jugador, indice)
            return "Esperando la selección del otro jugador..."

        else:
            self.generar_img_jugadas()
            self.actualizar_baraja(n_jugador, indice)
            ganador = self.determinar_ganador_ronda()
            self.duelo = {}

            if ganador != "=":
                return f"{self.jugadores.get(ganador)} ganó la ronda"

            else:
                return "Empate"

    def actualizar_baraja(self, n_jugador, indice):
        self.mazos.get(n_jugador).append(self.barajas.get(n_jugador).pop(indice))
        carta_nueva = self.mazos.get(n_jugador).pop(0)
        self.barajas.get(n_jugador)[indice] = carta_nueva

        ruta = self.obtener_ruta(carta_nueva)
        imagen_carta = Image.open(RUTA_CARTAS_JUEGO.format("o", ruta))
        imagen_baraja = Image.open(RUTA_BARAJAS.format("m", n_jugador))

        imagen_baraja.paste(imagen_carta, (self.posiciones[int(indice)], 100))
        imagen_baraja.save(RUTA_BARAJAS.format("m", n_jugador))

    def determinar_ganador_ronda(self):
        carta_j1 = self.duelo.get("1")
        carta_j2 = self.duelo.get("2")
        ganador_ronda = "="

        if self.debilidades.get(carta_j1.get("elemento")) == carta_j2.get("elemento"):
            ganador_ronda = "2"
            self.fichas.get("2").get(carta_j2.get("elemento")).append(carta_j2.get("color"))
            self.generar_img_ficha("2", carta_j2.get("elemento"), carta_j2.get("color"))
    
        elif self.debilidades.get(carta_j2.get("elemento")) == carta_j1.get("elemento"):
            ganador_ronda = "1"
            self.fichas.get("1").get(carta_j1.get("elemento")).append(carta_j1.get("color"))
            self.generar_img_ficha("1", carta_j1.get("elemento"), carta_j1.get("color"))

        elif carta_j1.get("puntos") > carta_j2.get("puntos"):
            ganador_ronda = "1"
            self.fichas.get("1").get(carta_j1.get("elemento")).append(carta_j1.get("color"))
            self.generar_img_ficha("1", carta_j1.get("elemento"), carta_j1.get("color"))

        elif carta_j2.get("puntos") > carta_j1.get("puntos"):
            ganador_ronda = "2"
            self.fichas.get("2").get(carta_j2.get("elemento")).append(carta_j2.get("color"))
            self.generar_img_ficha("2", carta_j2.get("elemento"), carta_j2.get("color"))

        return ganador_ronda
        
    def determinar_ganador_partida(self):
        fuego_j1, agua_j1, nieve_j1, ganador_j1_1 = self.comprobar_condicion_1("1")
        fuego_j2, agua_j2, nieve_j2, ganador_j2_1 = self.comprobar_condicion_1("2")

        ganador_j1_2 = self.comprobar_condicion_2("1", fuego_j1, agua_j1, nieve_j1)
        ganador_j2_2 = self.comprobar_condicion_2("2", fuego_j2, agua_j2, nieve_j2)

        if ganador_j1_1 or ganador_j1_2:
            self.generar_img_ganador("1")
            self.reiniciar_atributos()

            return "1"

        elif ganador_j2_1 or ganador_j2_2:
            self.generar_img_ganador("2")
            self.reiniciar_atributos()

            return "2"

    def reiniciar_atributos(self):
        self.jugadores = {}
        self.mazos = {}
        self.barajas = {}
        self.fichas = {"1": {"fuego": [], "agua": [], "nieve": []},
                    "2": {"fuego": [], "agua": [], "nieve": []}}
        self.posiciones_ficha = {"1": {"fuego": (21, 12), "agua": (105, 12), "nieve": (173, 12)},
                                "2": {"fuego": (920, 12), "agua": (840, 12), "nieve": (760, 12)}}

    def comprobar_condicion_1(self, n_jugador):
        colores_fuego = []
        colores_agua = []
        colores_nieve = []

        ganador = False
        for color in self.fichas.get(n_jugador).get("fuego"):
            if color not in colores_fuego:
                colores_fuego.append(color)

        for color in self.fichas.get(n_jugador).get("agua"):
            if color not in colores_agua:
                colores_agua.append(color)

        for color in self.fichas.get(n_jugador).get("nieve"):
            if color not in colores_nieve:
                colores_nieve.append(color)

        if len(colores_fuego) == 3 or len(colores_agua) == 3 or len(colores_nieve) == 3:
            ganador = True

        return (colores_fuego, colores_agua, colores_nieve, ganador)

    def comprobar_condicion_2(self, n_jugador, colores_fuego, colores_agua, colores_nieve):
        colores = []
        agregado_agua = False
        agregado_nieve = False
        ganador = False

        for color_fuego in colores_fuego: #se prueban todas las combinaciones posibles
            colores.append(color_fuego)

            for color_agua in colores_agua:

                if color_agua not in colores:
                    colores.append(color_agua)
                    agregado_agua = True

                for color_nieve in colores_nieve:

                    if color_nieve not in colores:
                        colores.append(color_nieve)
                        agregado_nieve = True

                    if len(colores) == 3 and not ganador: #C2: Condición 2
                        ganador = True
                        return ganador

                    elif agregado_nieve:
                        colores = colores[:-1]
                        agregado_nieve = False
                
                if agregado_agua:
                    colores = colores[:-1]
                    agregado_agua = False
        
            colores = colores[:-1]

    def generar_img_espera(self, n_jugador): 
        imagen_espera = Image.open(RUTA_IMAGEN_ESPERA.format("o", n_jugador))

        draw = ImageDraw.Draw(imagen_espera)
        font = ImageFont.truetype("arial.ttf", 30)

        draw.text(xy = (305, 540), text = self.jugadores.get("1"), fill = "black", font = font,
        stroke_width = 2, stroke_fill = "white")
        draw.text(xy = (630, 540), text = self.jugadores.get("2"), fill = "black", font = font,
        stroke_width = 2, stroke_fill = "white")

        imagen_espera.save(RUTA_IMAGEN_ESPERA.format("m", n_jugador))

    def generar_img_jugadas(self):
        imagen_jugadas = Image.open(RUTA_IMAGEN_JUGADAS.format("m"))
        draw = ImageDraw.Draw(imagen_jugadas)
        font = ImageFont.truetype("arial.ttf", 30)

        carta_j1 = self.duelo.get("1")
        ruta_j1 = self.obtener_ruta(carta_j1)

        carta_j2 = self.duelo.get("2")
        ruta_j2 = self.obtener_ruta(carta_j2)

        imagen_j1 = Image.open(RUTA_CARTAS_JUEGO.format("o", ruta_j1)) 
        imagen_j2 = Image.open(RUTA_CARTAS_JUEGO.format("o", ruta_j2))

        imagen_jugadas.paste(imagen_j1, (220, 155))
        imagen_jugadas.paste(imagen_j2, (548, 155))

        draw.text(xy = (305, 540), text = self.jugadores.get("1"), fill = "black", font = font,
        stroke_width = 2, stroke_fill = "white")
        draw.text(xy = (630, 540), text = self.jugadores.get("2"), fill = "black", font = font,
        stroke_width = 2, stroke_fill = "white")

        imagen_jugadas.save(RUTA_IMAGEN_JUGADAS.format("m"))

    def generar_img_ficha(self, n_jugador, elemento, color):
        imagen_jugadas = Image.open(RUTA_IMAGEN_JUGADAS.format("m"))
        imagen_espera_1 = Image.open(RUTA_IMAGEN_ESPERA.format("m", "1"))
        imagen_espera_2 = Image.open(RUTA_IMAGEN_ESPERA.format("m", "2"))

        ruta = elemento + "_" + color
        imagen_ficha = Image.open(RUTA_IMAGEN_FICHAS.format("o", ruta)) 
        imagen_ficha = imagen_ficha.resize((70, 58))

        posiciones = self.posiciones_ficha.get(n_jugador)
        imagen_jugadas.paste(imagen_ficha, (posiciones.get(elemento)[0], posiciones.get(elemento)[1]))
        imagen_espera_1.paste(imagen_ficha, (posiciones.get(elemento)[0], posiciones.get(elemento)[1]))
        imagen_espera_2.paste(imagen_ficha, (posiciones.get(elemento)[0], posiciones.get(elemento)[1]))

        nuevo_y = posiciones.get(elemento)[1] + 24
        self.posiciones_ficha.get(n_jugador)[elemento] = (posiciones.get(elemento)[0], nuevo_y)

        imagen_jugadas.save(RUTA_IMAGEN_JUGADAS.format("m"))
        imagen_espera_1.save(RUTA_IMAGEN_ESPERA.format("m", "1"))
        imagen_espera_2.save(RUTA_IMAGEN_ESPERA.format("m", "2"))

    def generar_img_ganador(self, n_jugador):
        imagen_victoria = Image.open(RUTA_IMAGEN_VICTORIA.format("o"))

        draw = ImageDraw.Draw(imagen_victoria)
        font = ImageFont.truetype("arial.ttf", 60)

        draw.text(xy = (260, 180), text = f"{self.jugadores.get(n_jugador)} ganó la partida!", 
        fill = "black", font = font, stroke_width = 3, stroke_fill = "white")

        imagen_victoria.save(RUTA_IMAGEN_VICTORIA.format("m"))
