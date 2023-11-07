from config import FFMPEG_OPTIONS, FFMPEG_ROUTE
from discord import FFmpegPCMAudio

class Playlist:
    def __init__(self):
        super().__init__()
        self.playlists = {}

    def add_song_to_playlist(self, guild_id: int, audio_url: str):
        if not self.playlists.get(guild_id):
            self.playlists[guild_id] = [audio_url]
        else:
            self.playlists.get(guild_id).append(audio_url)

    def play_song(self, voice_client, guild_id: int):
        if self.playlists.get(guild_id):
            audio_url = self.playlists.get(guild_id).pop(0)

            voice_client.play(FFmpegPCMAudio(executable=FFMPEG_ROUTE, source=audio_url, options=FFMPEG_OPTIONS), after=lambda: self.play_song(voice_client, guild_id))

    def skip_song(self, voice_client, guild_id: int):
        if (not self.playlists.get(guild_id)) or len(self.playlists.get(guild_id)) < 1:
            return "{}, no hay más elementos en cola"

        voice_client.stop()
        self.play_song(voice_client, guild_id)

        return "{} saltó la canción"
