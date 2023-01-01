from discord import Interaction, Color, File, ButtonStyle
from discord.ui import View, button, Button
from PIL import Image

from tuliojitsu.parametros import RUTA_BARAJAS, RUTA_IMAGEN_JUGADAS, \
                                RUTA_IMAGEN_ESPERA, RUTA_IMAGEN_VICTORIA

class Resultado(View):
    def __init__(self, tuliojitsu, jugadores, barajas):
        super().__init__()
        self.tuliojitsu = tuliojitsu #instancia de la clase Tuliojitsu
        self.jugadores = jugadores #diccionario con el número y el nombre del jugador
        self.barajas = barajas #diccionario con las barajas de cada jugador
        self.value = None
        self.timeout = None
        self.reiniciar_dojo()

    @button(label = "Mostrar baraja", style = ButtonStyle.primary)
    async def boton(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"):
            view = Eleccion(self.tuliojitsu, self.jugadores, self.barajas, self)

            file = File(RUTA_BARAJAS.format("m", "1")) 
            await interaction.response.send_message(file = file, ephemeral = True, view = view)

        elif interaction.user.name == self.jugadores.get("2"):
            view = Eleccion(self.tuliojitsu ,self.jugadores, self.barajas, self)

            file = File(RUTA_BARAJAS.format("m", "2"))
            await interaction.response.send_message(file = file, ephemeral = True, view = view)

        else:
            await interaction.response.send_message("No formas parte del duelo! D:", ephemeral = True)

    def reiniciar_dojo(self):
        imagen_original = Image.open(RUTA_IMAGEN_JUGADAS.format("o")) #hacer función sobre esto
        imagen_modificada = Image.open(RUTA_IMAGEN_JUGADAS.format("m"))
        imagen_modificada.paste(imagen_original, (0, 0))
        imagen_modificada.save(RUTA_IMAGEN_JUGADAS.format("m"))

        imagen_original = Image.open(RUTA_IMAGEN_ESPERA.format("o", "1"))
        imagen_modificada = Image.open(RUTA_IMAGEN_ESPERA.format("m", "1"))
        imagen_modificada.paste(imagen_original, (0, 0))
        imagen_modificada.save(RUTA_IMAGEN_ESPERA.format("m", "1"))

        imagen_original = Image.open(RUTA_IMAGEN_ESPERA.format("o", "2"))
        imagen_modificada = Image.open(RUTA_IMAGEN_ESPERA.format("m", "2"))
        imagen_modificada.paste(imagen_original, (0, 0))
        imagen_modificada.save(RUTA_IMAGEN_ESPERA.format("m", "2"))

        self.tuliojitsu.generar_img_espera("1")
        self.tuliojitsu.generar_img_espera("2")

class Eleccion(View):
    def __init__(self, tuliojitsu, jugadores, barajas, view):
        super().__init__()
        self.tuliojitsu = tuliojitsu
        self.jugadores = jugadores
        self.barajas = barajas
        self.view = view
        self.duelo = {} #diccionario que posee las cartas jugadas por cada jugador
        self.value = None
        self.timeout = None

    @button(label = "1", style = ButtonStyle.primary)
    async def carta_1(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"): #haria esto de acá una función, pero el parametro "interaction" solo existe dentro de este segmento para cada decorador
            respuesta = self.tuliojitsu.manejar_duelo("1", "0")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "1")) 

                await interaction.response.send_message(respuesta, file = file)    

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

        elif interaction.user.name == self.jugadores.get("2"):
            respuesta = self.tuliojitsu.manejar_duelo("2", "0")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "2")) 

                await interaction.response.send_message(respuesta, file = file)  

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

    @button(label = "2", style = ButtonStyle.primary)
    async def carta_2(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"): #haria esto de acá una función, pero el parametro "interaction" solo existe dentro de este segmento para cada decorador
            respuesta = self.tuliojitsu.manejar_duelo("1", "1")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "1")) 

                await interaction.response.send_message(respuesta, file = file)  

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

        elif interaction.user.name == self.jugadores.get("2"):
            respuesta = self.tuliojitsu.manejar_duelo("2", "1")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "2")) 

                await interaction.response.send_message(respuesta, file = file)

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

    @button(label = "3", style = ButtonStyle.primary)
    async def carta_3(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"): #haria esto de acá una función, pero el parametro "interaction" solo existe dentro de este segmento para cada decorador
            respuesta = self.tuliojitsu.manejar_duelo("1", "2")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "1")) 

                await interaction.response.send_message(respuesta, file = file) 

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

        elif interaction.user.name == self.jugadores.get("2"):
            respuesta = self.tuliojitsu.manejar_duelo("2", "2")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "2")) 

                await interaction.response.send_message(respuesta, file = file) 

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

    @button(label = "4", style = ButtonStyle.primary)
    async def carta_4(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"): #haria esto de acá una función, pero el parametro "interaction" solo existe dentro de este segmento para cada decorador
            respuesta = self.tuliojitsu.manejar_duelo("1", "3")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "1")) 

                await interaction.response.send_message(respuesta, file = file)   

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

        elif interaction.user.name == self.jugadores.get("2"):
            respuesta = self.tuliojitsu.manejar_duelo("2", "3")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "2")) 

                await interaction.response.send_message(respuesta, file = file)

            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

    @button(label = "5", style = ButtonStyle.primary)
    async def carta_5(self, interaction: Interaction, button: Button):
        if interaction.user.name == self.jugadores.get("1"): #haria esto de acá una función, pero el parametro "interaction" solo existe dentro de este segmento para cada decorador
            respuesta = self.tuliojitsu.manejar_duelo("1", "4")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "1")) 

                await interaction.response.send_message(respuesta, file = file)
            
            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

        elif interaction.user.name == self.jugadores.get("2"):
            respuesta = self.tuliojitsu.manejar_duelo("2", "4")

            if respuesta == "Esperando la selección del otro jugador...":
                file = File(RUTA_IMAGEN_ESPERA.format("m", "2")) 

                await interaction.response.send_message(respuesta, file = file)
            
            else:
                file = File(RUTA_IMAGEN_JUGADAS.format("m")) 
                files = [file]

                ganador = self.tuliojitsu.determinar_ganador_partida()
                if ganador != None:
                    respuesta, files = self.manejar_ganador(ganador, files)

                await interaction.response.send_message(respuesta, files = files , view = self.view)

    def manejar_ganador(self, ganador, files):
        file = File(RUTA_IMAGEN_VICTORIA.format("m"))
        files.append(file)
        self.view = View()
        return (f"{self.jugadores.get(ganador)} ganó la partida!", files)
