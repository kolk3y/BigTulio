from config import TOKEN, FFMPEG_OPTIONS, YOUTUBE_SEARCH, FFMPEG_ROUTE, YOUTUBE_REGEX, YOUTUBE_RESULTS
import pafy
import urllib
import re
from discord import Intents, Interaction, FFmpegPCMAudio
from discord.ext import commands
from tuliojitsu.tuliojitsu import Tuliojitsu
from tuliojitsu.menus import Resultado
from reactions.reactions import Reactions
from playlist import Playlist

bot = commands.Bot(command_prefix = "!", intents = Intents.all())

tuliojitsu = Tuliojitsu()
reactions = Reactions()
playlist = Playlist()

@bot.event
async def on_ready():
    print("Online")

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name = "tuliojitsu", description= "Comienza una partida de tuliojitsu")
async def tuliojitsu_game(interaction: Interaction):
    respuesta = tuliojitsu.sala_espera(interaction.user.name)

    if "Comenzando la partida entre" not in respuesta:
        await interaction.response.send_message(respuesta)

    else:
        view = Resultado(tuliojitsu, tuliojitsu.jugadores, tuliojitsu.barajas)

        await interaction.response.send_message(respuesta, view = view)  

async def handle_reaction(interaction: Interaction):
    respuesta = reactions.get_reaction(interaction.user.name, interaction.command.name)

    await interaction.response.send_message(embed=respuesta)

@bot.tree.command(name="laugh", description="Expresa tu risa")
async def happy_reaction(interaction: Interaction):
    await handle_reaction(interaction)

@bot.tree.command(name="bye", description="Despídete de tus camaradas")
async def bye_reaction(interaction: Interaction):
    await handle_reaction(interaction)

@bot.tree.command(name="floppa", description="Trae a la gran criatura")
async def floppa_reaction(interaction: Interaction):
    await handle_reaction(interaction)

@bot.tree.command(name="play", description="Reproducir música de YouTube")
async def play_youtube(interaction: Interaction, music: str):
    """
    Parameters
    -----------
    music: str
        La canción a reproducir
    """
    voice_client = interaction.guild.voice_client
    voice_user = interaction.user.voice

    if not voice_user:
        return await interaction.response.send_message("Debes estar conectado a un canal de voz!")
    elif not voice_client:
        await voice_user.channel.connect(self_deaf=True)
        voice_client = interaction.guild.voice_client #Se redefine con la información de la conexión

    query = music.replace(" ", "+")
    html = urllib.request.urlopen(YOUTUBE_SEARCH + query)
    video_ids = re.findall(YOUTUBE_REGEX, html.read().decode())
    video_url = YOUTUBE_RESULTS + video_ids[0]

    song = pafy.new(video_ids[0])  
    audio_url = song.getbestaudio().url  
    playlist.add_song_to_playlist(interaction.guild_id, audio_url)

    if voice_client.is_playing() or voice_client.is_paused():    
        await interaction.response.send_message("Se agregó la canción a la playlist \n {}".format(video_url))
    else:
        await interaction.response.send_message(video_url)
        playlist.play_song(voice_client, interaction.guild_id)

@bot.tree.command(name="pause-resume", description="Pausar-Reanudar la reproducción de música")
async def pause_music(interaction: Interaction):
    voice_client = interaction.guild.voice_client

    if not voice_client:
        await interaction.response.send_message("No hay música reproduciéndose")
    elif voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("{} ha pausado la canción".format(interaction.user.name))
    elif voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("{} ha reanudado la canción".format(interaction.user.name))

@bot.tree.command(name="stop", description="Detener la reproducción de música")
async def stop_music(interaction: Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

        await interaction.response.send_message("{} ha detenido la reproducción de música".format(interaction.user.name))

@bot.tree.command(name="skip", description="Salta a la siguiente canción de la playlist")
async def skip_music(interaction: Interaction):
    voice_client = interaction.guild.voice_client

    if voice_client.is_playing() or voice_client.is_paused():
        response = playlist.skip_song(voice_client, interaction.guild_id)

        await interaction.response.send_message(response.format(interaction.user.name))
    else:
        interaction.response.send_message("No hay canciones en reproducción")

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.bot and before.channel and not after.channel:
        # El miembro se desconectó del canal de voz, detener la reproducción si es necesario.
        voice_client = member.guild.voice_client
        if voice_client:
            if not any(voice_member != member for voice_member in voice_client.channel.members):
                # Nadie más en el canal de voz, detener la reproducción.
                voice_client.stop()

bot.run(TOKEN)
