# ---Imports---#
import json
import os
import time
import discord
import discord.utils
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, Bot
import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ---Set up Admin Class---#
class Formula1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Formula 1 Cog Loaded!")
        print("-----------------------------------------------")

    # ---F1 Schedule---#
    @commands.hybrid_command()
    async def racecalendar(self, ctx):
        # Get current years F1 Schedule and make arrays for each data field
        currentYear = datetime.now().year
        schedule = fastf1.get_event_schedule(currentYear, include_testing=True, backend='fastf1')
        eventName = pd.unique(schedule.EventName)
        eventDate = pd.unique(schedule.Session5DateUtc)

        # Remove the first entry from each array (Unneeded info)
        eventName = eventName[1:]
        eventDate = eventDate[1:]

        # Strip the trailing zeros and extra characters from the dateTime Array
        dateTimeArray = np.core.defchararray.chararray.rstrip(
            np.core.defchararray.chararray.rstrip(
                np.core.defchararray.chararray.rstrip(
                    np.core.defchararray.chararray.rstrip(
                        eventDate.astype(str), '0'
                    ).astype(str), '.'
                ).astype(str), '0'
            ).astype(str), ':'
        )
        # Remove the T from the date array, and replace it with spacing
        dateTimeArray = np.core.defchararray.chararray.replace(dateTimeArray.astype(str), 'T', ' ')

        # Split up the time and date from dateTime Array
        splitArrays = np.char.split(dateTimeArray)
        # Extract the time from split Arrays
        timeArray = np.array([split[-1] for split in splitArrays], dtype=np.str_)
        # Remove the times from the original Array
        dateArray = np.array([' '.join(split[:-1]) for split in splitArrays], dtype=np.str_)
        # Replace 'Grand Prix' with 'GP' to make the Discord Embed smaller
        eventArray = np.core.defchararray.chararray.replace(eventName.astype(str), 'Grand Prix', 'GP')

        # Convert the UTC time to PST
        def convert_utc_to_pst(utc_time):
            # Convert string to a datetime object
            utc_datetime = datetime.strptime(utc_time, "%H:%M")
            # Convert to PST
            pst_datetime = utc_datetime - timedelta(hours=8)
            # Convert the 24-Hour time to 12-Hour Time with AM&PM
            pst_time = pst_datetime.strftime("%I:%M %p")
            return pst_time

        # Find the next race in the schedule
        def index_closest_date(date_array):
            # Get the current date and time
            current_datetime = datetime.now()
            # Convert date array strings to datetime objects
            date_objects = np.array([datetime.strptime(date, '%Y-%m-%d') for date in date_array])
            # Find the index of the closest date to the current date
            date_index = np.argmin(np.abs(date_objects - current_datetime))
            return date_index

        # Emphasize/Format the Next Race
        # First Column (Event Name (GP))
        def format_next_race_name(value):
            return f'➡️**{value}**'
        # Second Column (Event Date)
        def format_next_race_date(value):
            return f'**{value}**'
        # Third Column (Event Time)
        def format_next_race_time(value):
            return f'**{value}**⬅️'

        # Convert date from 'YYYY-MM-DD' format to 'shortMonth. DD'
        def format_date(utc_date):
            # Convert string to a datetime object
            date_object = datetime.strptime(utc_date, "%Y-%m-%d")
            formatted_date = date_object.strftime('%b %d')
            return formatted_date

        # ---Call the Next Race function---#
        nextRaceIndex = index_closest_date(dateArray)

        # ---Call the UTC to PST Function---#
        # Vectorize the convert_utc_to_pst function
        vectorizedConvert_Time = np.vectorize(convert_utc_to_pst)
        # Apply the vectorized function to the UTC times array
        pstTimeArray = vectorizedConvert_Time(timeArray)

        # ---Call the Format Date Function---#
        # Vectorize the convert_utc_to_pst function
        vectorizedConvert_Date = np.vectorize(format_date)
        # Apply the vectorized function to the UTC times array
        formattedDateArray = vectorizedConvert_Date(dateArray)

        # Build Pandas dataframe
        data = {'**Event, ': eventArray,
                'Date, ': formattedDateArray,
                ' & Time (PST)**': pstTimeArray
                }
        dataFrame = pd.DataFrame(data)

        # Call format_next_race for all 3 columns
        # Name
        dataFrame['**Event, '] = dataFrame['**Event, '].apply(
            lambda x: format_next_race_name(x) if x == dataFrame.at[nextRaceIndex, '**Event, '] else x)
        # Date
        dataFrame['Date, '] = dataFrame['Date, '].apply(
            lambda x: format_next_race_date(x) if x == dataFrame.at[nextRaceIndex, 'Date, '] else x)
        # Time
        dataFrame[' & Time (PST)**'] = dataFrame[' & Time (PST)**'].apply(
            lambda x: format_next_race_time(x) if x == dataFrame.at[nextRaceIndex, ' & Time (PST)**'] else x)

        # Make the array start at one to maintain proper Race ordering/numbering

        dataFrame.index = dataFrame.index + 1

        # Put final dataframe into a discord embed and send it
        embed = discord.Embed(title=str(currentYear) + " F1 Race Calendar", description=dataFrame, color=0xfa0c0c)
        embed.set_thumbnail(url="https://www.formula1.com/etc/designs/fom-website/social/f1-default-share.jpg")
        await ctx.send(embed=embed)


# ---Setup the cogs---#
async def setup(bot):
    await bot.add_cog(Formula1(bot))
