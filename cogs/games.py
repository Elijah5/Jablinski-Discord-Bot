# ---Imports---#
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
import re
import time
from random import randint
import datetime
import asyncio


# ---Set up Games Class---#
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games Cog Loaded!")
        print("-----------------------------------------------")

    ###Coin Flipper Game###
    @commands.hybrid_command()
    async def coin(self, ctx):
        coin = randint(1, 2)
        if coin == 1:
            heads = True
        else:
            heads = False
        if heads == True:
            await ctx.send("It's Heads!")
        else:
            await ctx.send("It's Tails")

    # ---Roulette---#
    ###Function and Variable Define###=
    def roulette(rnumber):
        global lose
        rInput = rnumber
        roulette = randint(1, (7 - rInput))
        ###Roulette Logic###
        if roulette == 1:
            lose = True
        else:
            lose = False
            return lose

    ###Roulette Game###
    @commands.hybrid_command()
    async def roulette(self, ctx, ramount):
        rouletteNumber = int(ramount)
        ###Roulette Needs to be In-between 1 and 6###
        if rouletteNumber > 6:
            await ctx.send("```Usage:\n >roulette (1,6)```")
        elif rouletteNumber < 1:
            await ctx.send("```Usage:\n >roulette (1,6)```")
        elif rouletteNumber == 6:
            await ctx.send("That doesn't seem like the best idea...")
        else:
            if lose == True:
                await ctx.send("*BANG!* Well that was a bad idea")

    @roulette.error
    async def roulette_error(error, ctx, self):
        errorWin = randint(1, 2)
        if errorWin == 1:
            await ctx.send("*Click* Nothing happened")
        if errorWin == 2:
            await ctx.send("*BANG!* Well that was a bad idea")

    @commands.hybrid_command()
    async def remind(self, ctx, thours, tminutes, *, tremind):

        timerUser = ctx.author.mention
        strtHours = str(thours)
        strtMinutes = str(tminutes)
        inttHours = int(thours)
        inttMins = int(tminutes)
        await ctx.send("Timer Set! I will remind you to `" + str(tremind) + "` in `" + strtHours + "hr" + strtMinutes + "min`")
        ###Convert Hours and Minutes into Seconds for async sleep###
        hourSeconds = inttHours * 3600
        minSeconds = inttMins * 60
        secondsFinal = hourSeconds + minSeconds
        intsecondsFinal = int(secondsFinal)
        await asyncio.sleep(secondsFinal)
        await ctx.send(
            timerUser + " Your `" + strtHours + "h" + strtMinutes + "m` timer is going off! " + "Reminder: `" + str(
                tremind) + "`")

    @remind.error
    async def timer_error(error, ctx, self):
        await ctx.send(
            "That didn't work... \n \n ```Usage: \n  >remind {hours} {minutes} {reminder}```"
        )


async def setup(bot):
    await bot.add_cog(Games(bot))
