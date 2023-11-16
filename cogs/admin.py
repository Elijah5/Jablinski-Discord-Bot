#---Imports---#
import json
import os
import time
import discord
import discord.utils
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, Bot
from dotenv import load_dotenv


#---Set up Admin Class---#
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Cog Loaded!")
        print("-----------------------------------------------")

    # ---Purge Messages---#
    @commands.hybrid_command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, messagesamount):
        ###Make messagesamount an int, and add 1 to Delete Your Message Too###
        messagesamount = int(messagesamount)
        strmessagesamount = str(messagesamount)
        messagesamount += 1
        ###messagesamount Needs to be In-between 1-99###
        if messagesamount > 101 or messagesamount < 1:
            await ctx.send(
                "Bad Arguments!\n ```Usage:\n  >purge(1,100)\n \n   Note: You can only delete up to 100 messages, "
                "that are no older than 14 days```"
            )
        ###If Arguments are Correct, Run Purge, and Limit to pAmount###
        else:
            await ctx.send("Purging `" + strmessagesamount + "` Messages!")
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=messagesamount)
            await ctx.send("Deleted `" + strmessagesamount + "` Messages!")

    #---Ban Timer---#
    @commands.hybrid_command()
    @has_permissions(administrator=True)
    async def bantimer(self, ctx, member: discord.Member, banhour, banmin, *, banreason):
        intbanHour = int(banhour)
        intbanMin = int(banmin)
        ###Convert Hours and Minutes into Seconds for async sleep###
        hourtoSeconds = intbanHour * 3600
        mintoSeconds = intbanMin * 60
        finalSeconds = hourtoSeconds + mintoSeconds
        intfinalSeconds = int(finalSeconds)

        if banreason == "":
            banreason = "No reason given"
        mentionUser = member.mention
        await ctx.send(mentionUser + " will be banned for ```" + banhour + "Hr" + banmin + "Min```")
        await member.ban(reason=banreason)
        await asyncio.sleep(intfinalSeconds)

    @bantimer.error
    async def bantimer_error(error, ctx, self):
        await ctx.send(
            "Improper syntax or permissions! \n \n ```Usage: \n  >bantimer {user} {hours} {minutes} {reason}```")

    #---Temp-ban---#
    @commands.hybrid_command()
    @has_permissions(administrator=True)
    async def tempban(self, ctx, member: discord.Member, bhour, bmin, *, reason):
        intbHour = int(bhour)
        intbMin = int(bmin)
        serverName = member.guild.name
        link = await ctx.channel.create_invite(max_age=100000)
        ###Convert Hours and Minutes into Seconds for async sleep###
        hourSeconds = intbHour * 3600
        minSeconds = intbMin * 60
        secondsFinal = hourSeconds + minSeconds
        intsecondsFinal = int(secondsFinal)

        if reason == "":
            reason = "No reason given"
        mentionUser = member.mention
        await ctx.send(mentionUser + " is temporarily banned for ```" + bhour + "Hr" + bmin + "Min```")
        await member.send(
            "You have been banned from " + serverName + " for ```" + bhour + "Hr" + bmin + "Min```" + "Reason: " + reason + "\n When you are unbanned, click the link to join")
        await member.send(link)
        await member.ban(reason=reason)
        await asyncio.sleep(intsecondsFinal)
        await ctx.guild.unban(member)
        await ctx.send(mentionUser + " Has been unbanned")

    @tempban.error
    async def tempban_error(error, ctx, self):
        await ctx.send(
            "Improper syntax or permissions! \n \n ```Usage: \n  >tempban {user} {hours} {minutes} {reason}```")


#---Setup the cogs---#
async def setup(bot):
    await bot.add_cog(Admin(bot))
