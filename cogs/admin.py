#---Imports---#
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
import re
import time
import asyncio
import datetime


#---Set up Admin Class---#
class Admin(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog Loaded!")
        print("-----------------------------------------------")

    #---Purge Messages---#
    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, pAmount):
        ###Make pAmount an int, and add 1 to Delete Your Message Too###
        pAmount = int(pAmount)
        strpAmount = str(pAmount)
        pAmount += 1
        ###pAmount Needs to be Inbetween 1-99###
        if pAmount > 101 or pAmount < 1:
            await ctx.send(
                "Bad Arguments!\n ```Usage:\n  >purge(1,100)\n \n   Note: You can only delete up to 100 messages, that are no older than 14 days```"
            )
        ###If Agruments are Correct, Run Purge, and Limit to pAmount###
        else:
            await ctx.send("Purging `" + strpAmount + "` Messages!")
            time.sleep(3)
            await ctx.message.delete()
            time.sleep(0.2)
            await ctx.channel.purge(limit=pAmount)
            await ctx.send("Deleted `" + strpAmount + "` Messages!")

    #---Ban Timer---#
    @commands.command()
    @has_permissions(administrator=True)
    async def bantimer(self, ctx, member: discord.Member, banHour, banMin, *, banReason):
        intbanHour = int(banHour)
        intbanMin = int(banMin)
        ###Convert Hours and Minutes into Seconds for async sleep###
        hourtoSeconds = intbanHour * 3600
        mintoSeconds = intbanMin * 60
        finalSeconds = hourtoSeconds + mintoSeconds
        intfinalSeconds = int(finalSeconds)

        if banReason == "":
            banReason = "No reason given"
        mentionUser = member.mention
        await ctx.send(mentionUser + " will be banned for ```" + banHour + "Hr" + banMin + "Min```")
        await member.ban(reason=banReason)
        await asyncio.sleep(intfinalSeconds)

    @bantimer.error
    async def bantimer_error(error, ctx, self):
        await ctx.send(
            "Improper syntax or permissions! \n \n ```Usage: \n  >bantimer {user} {hours} {minutes} {reason}```")

    #---Tempban---#
    @commands.command()
    @has_permissions(administrator=True)
    async def tempban(self, ctx, member: discord.Member, bHour, bMin, *, reason):
        intbHour = int(bHour)
        intbMin = int(bMin)
        serverName = member.guild.name
        link = await ctx.channel.create_invite(max_age = 100000)
        ###Convert Hours and Minutes into Seconds for async sleep###
        hourSeconds = intbHour * 3600
        minSeconds = intbMin * 60
        secondsFinal = hourSeconds + minSeconds
        intsecondsFinal = int(secondsFinal)

        if reason == "":
            reason = "No reason given"
        mentionUser = member.mention
        await ctx.send(mentionUser + " is temporarily banned for ```" + bHour + "Hr" + bMin + "Min```")
        await member.send("You have been banned from " + serverName + " for ```" + bHour + "Hr" + bMin + "Min```" + "Reason: " + reason + "\n When you are unbanned, click the link to join")
        await member.send(link)
        await member.ban(reason=reason)
        await asyncio.sleep(intsecondsFinal)
        await ctx.guild.unban(member)
        await ctx.send(mentionUser + " Has been unbanned")


    @tempban.error
    async def tempban_error(error, ctx, self):
        await ctx.send(
            "Improper syntax or permissions! \n \n ```Usage: \n  >tempban {user} {hours} {minutes} {reason}```")

###Setup the cogs###
def setup(bot):
    bot.add_cog(Admin(bot))
