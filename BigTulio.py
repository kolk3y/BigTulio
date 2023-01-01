from config import TOKEN
from discord import Intents, Interaction
from discord.ext import commands
from tuliojitsu.tuliojitsu import Tuliojitsu
from tuliojitsu.menus import Resultado

bot = commands.Bot(command_prefix = "!", intents = Intents.all())

tuliojitsu = Tuliojitsu()

@bot.event
async def on_ready():
    print("Online")

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name = "tuliojitsu")
async def tuliojitsu_game(interaction: Interaction):
    respuesta = tuliojitsu.sala_espera(interaction.user.name)

    if "Comenzando la partida entre" not in respuesta:
        await interaction.response.send_message(respuesta)

    else:
        view = Resultado(tuliojitsu, tuliojitsu.jugadores, tuliojitsu.barajas)

        await interaction.response.send_message(respuesta, view = view)  

bot.run(TOKEN)
