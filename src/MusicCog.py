import asyncio
import json

import discord
from discord.ext import commands
from yandex_music import Client

def get_token(token_name):
    with open("config/config_my.json", "r", encoding="utf8") as file:
        conf = json.load(file)
    return conf[token_name]

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = discord.VoiceChannel

        self.yandex_client = Client(get_token("yandex_token"))
        self.yandex_client.init()

        self.yandex_count = 0

        self.path = "data/"

        self.is_playing = False
        self.is_paused = False
        self.is_joined = False

        self.music_queue = []

        self.voice_client = None

    @commands.hybrid_command(name='play')
    async def play(self, ctx):
        # grab the user who sent the command
        self.is_playing = True
        user = ctx.message.author
        self.voice_client = user.voice.channel
        channel = None
        # only play music if user is in a voice channel
        if self.voice_client is not None:
            # grab user's voice channel
            channel = self.voice_client.name
            await ctx.send('User is in channel: ' + channel)

            # create StreamPlayer
            if not self.is_joined:
                self.vc = await self.voice_client.connect()

            def after(error):
                self.yandex_count += 1
                url = f"example_{self.yandex_count}.mp3"
                self.yandex_client.users_likes_tracks()[self.yandex_count].fetch_track().download(url)
                next_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
                ctx.voice_client.play(next_source, after=after)

            # while self.is_playing:
            url = f"example_{self.yandex_count}.mp3"
            self.yandex_client.users_likes_tracks()[self.yandex_count].fetch_track().download(url)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
            self.vc.play(source, after=after)

            while not self.vc.is_done():
                await asyncio.sleep(1)
            self.yandex_count += 0

            # disconnect after the player has finished
            self.vc.stop()
            self.is_playing = False
            await self.vc.disconnect()
        else:
            await ctx.send('User is not in a channel.')

    @commands.hybrid_command(name='join')
    async def _join(self, ctx: commands.Context):
        """Подключается к голосовому каналу."""
        channel = ctx.author.voice.channel
        self.is_joined = True
        self.vc = await channel.connect()

    @commands.hybrid_command(name='join_with_token')
    async def _join_token(self, ctx: commands.Context, token):
        """Подключается к голосовому каналу."""
        self.yandex_client = Client(token)
        self.yandex_client.init()
        channel = ctx.author.voice.channel
        self.is_joined = True
        self.vc = await channel.connect()

    @commands.hybrid_command(name='pause')
    async def pause(self, ctx):
        self.is_playing = False

    @commands.hybrid_command(name='leave')
    async def leave(self, ctx):
        self.is_playing = False
        self.is_joined = False
        await ctx.voice_client.disconnect()
