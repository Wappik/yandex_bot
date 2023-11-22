import os
import asyncio

import discord
from discord.ext import commands

from src.MusicCog import MusicCog, get_token

ROOT = os.path.dirname(__file__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description='A music bot.',
    intents=intents,
    # intents=discord.Intents.all(),
    case_insensitive=True,
    self_bot=True
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync()


async def main():
    async with bot:
        await bot.add_cog(MusicCog(bot))
        await bot.start(get_token('discord_token'))


asyncio.run(main())

