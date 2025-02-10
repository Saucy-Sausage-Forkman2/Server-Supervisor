import asyncio
import discord
import json
import os
import datetime

red = discord.Colour.red()
green = discord.Colour.green()
blue = discord.Colour.blue()
darkRed = discord.Colour.dark_red()
fuchsia = discord.Colour.fuchsia()

def time():
    """Generates a timestamp of the current time in the PST timezone.

    Returns:
        string: A timestamp in the form of HOUR:MINUTE AM/PM PST
    """
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    pm = ' AM'
    if hour >= 12:
        pm = " PM"
    if hour >= 13:
        hour -= 12
    if hour == 0:
    	hour = 12
    if minute < 10:
        minute = "0" + str(minute)

    return f"{hour}" + ":" + f"{minute}"  + f"{pm}" + "  PST"

def format_ark(arkServerQuery2DArray, arkAllServersOfflineTitle="Ark: Offline",arkAllServersOnlineTitle="Ark"):
    arkFormattedPlayers = ""
    embed = 0
    
    arkEmbedFields = []

    if arkServerQuery2DArray == []:
        embed = discord.Embed(
            title=arkAllServersOfflineTitle,
            color=red
            )
    else:
        for arkServerInfoArray in arkServerQuery2DArray:

            if type(arkServerInfoArray) != list:
                arkEmbedFields.append(arkServerInfoArray)
                continue

            #0 address, 1 serverInfo, 2 serverPlayers
            arkServerInfo = arkServerInfoArray[1]

            arkServerName = arkServerInfo.server_name
            arkMapName = arkServerInfo.map_name
            arkPlayerCount = arkServerInfo.player_count
            
            match(arkServerName):
                case "TheIsland": 
                    arkServerName="The Island"

            arkEmbedFieldTemplate = f"{arkServerName[:-12]} ({arkMapName}): {arkPlayerCount}"
            arkEmbedFields.append(arkEmbedFieldTemplate)

        embed = discord.Embed(
            title=arkAllServersOnlineTitle,
            color=fuchsia
            )

        for arkEmbedPair in arkEmbedFields:
            embed.add_field(name=arkEmbedPair,value="")

        
    embed.set_footer(text=time())
    return embed

def format_palworld(palworldInfo, palworldPlayers, palworldAddress, palworldOnlineTitle="Palworld", palworldOfflineTitle="Palworld Offline"):
    embed = discord.Embed(
        title=palworldOfflineTitle,
        color=darkRed,
    )

    if palworldInfo != 1:
        embed = discord.Embed(
            title=palworldOnlineTitle,
            color=blue,
        )

        palworldVersion = palworldInfo.version
        embed.add_field(name="", value=f"{palworldVersion}")
        embed.add_field(name="", value=palworldAddress,inline=True)
        
        if javaPlayerList != None:        
            for player in javaPlayerList:

                match(player.name):
                        
                    case _:
                        formattedUsernames += " " + i.name + "\n"

                        embed.add_field(name="", value="",inline=False)
                        embed.add_field(name="Players", value="")
                        embed.add_field(name="", value=formattedUsernames,inline=True)


    embed.set_footer(text=time())
    return embed

def format_minecraft(java, category, javaAddress, javaOnlineTitle="Minecraft", javaOfflineTitle="Minecraft: Offline"):
    embed = discord.Embed(
        title=javaOfflineTitle,
        color=red,
    )

    if type(java) != Exception:
        embed = discord.Embed(
        title=javaOnlineTitle,
        color=green,
        )

        javaVersion = java.version.name
        javaPlayerList = java.players.sample
            
        embed.add_field(name="", value=f"{javaVersion}")
        embed.add_field(name="", value=javaAddress,inline=True)

        if javaPlayerList != None:        
            for player in javaPlayerList:
                match(player.name):

                    case "ItsSquishy173": 
                        continue        
                        
                    case _:
                        formattedUsernames += " " + i.name + "\n"

                        embed.add_field(name="", value="",inline=False)
                        embed.add_field(name="Players", value="")
                        embed.add_field(name="", value=formattedUsernames,inline=True)


    embed.set_footer(text=time())
    return embed