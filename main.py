# ---Imports---#
import os
import time
import aiohttp
import asyncio
import logging
import discord
import discord.utils
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, Bot

#---Setup Enviroment Variables---#
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#---Discord.py Def---#
intents = discord.Intents.all()
intents.message_content = True
bot: Bot = commands.Bot(command_prefix='>', intents=intents)


#---Print When Ready---#
@bot.event
async def on_ready():
    print("-----------------------------------------------")
    print("Bot Is Online!")
    print("-----------------------------------------------")
    await bot.change_presence(activity=discord.Game(name='>help'))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(e)


#---Load The Cogs---#
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


#---Ping delay test---#
@bot.hybrid_command()
async def ping(ctx):
    latency = bot.latency
    msLatency = latency * 1000
    strLatency = str(msLatency)
    roundLatency = strLatency[0:5]
    await ctx.send("Pong! `(" + roundLatency + " ms)`")


#---Logging---#
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level=logging.INFO, root=False)


#---Startup---#
async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
