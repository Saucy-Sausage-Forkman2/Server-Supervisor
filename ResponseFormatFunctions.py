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
    """Takes in the results of each server in the cluster and formats them into one embed.

    Args:
        arkServerQuery2DArray (list[][]): A 2D array that contains the address, information, and player count, respectively, of each cluster in each subarray. To indicate an error, the subarray for a server should instead be anything but an array.
        arkAllServersOfflineTitle (str, optional): The title of the embed to be used when the server is offline. Defaults to "Ark: Offline".
        arkAllServersOnlineTitle (str, optional): The title of the embed to be used when the server is online. Defaults to "Ark".

    Returns:
        (discord.Embed): An embed that shows the server names, addresses, and the number of online players in each server.
    """

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

def format_palworld(palworldInfo,palworldPlayers,palworldAddress, palworldOnlineTitle="Palworld", palworldOfflineTitle="Palworld: Offline"):
    """Formats the server response and address into a discord embed. Errors are included in the palworldInfo parameter givin by the palworld_api library, so no exceptions need to be made in the parameters to indiciate server outages to the function.

    Args:
        palworldInfo (dict): The dictionary of the server status given by palworld_api library.
        palworldPlayers (dict): The dictionary that shows the online players given by palworld_api library.
        palworldAddress (str): The server address to be displayed in the embed.
        palworldOnlineTitle (str, optional): The title of the embed to be used when the server is online. Defaults to "Palworld".
        palworldOfflineTitle (str, optional): The title of the embed to be used when the server is offline. Defaults to "Palworld: Offline".

    Returns:
        (discord.Embed): An embed that shows the server name, version, address, and online players.
    """

    embed = discord.Embed(
        title=palworldOfflineTitle,
        color=darkRed,
        description="The Server is Offline."
        )

    try:   
        #If the palworld server is down, the library will return a dictionary with the single entry of 'error'. In this case, we check to see if the dictionary contains
        # any key for error. If it does, that means the server is inaccessible.
        if palworldInfo['error']:
            pass

    except:
        #this runs if there is no error, both in connecting to the server and in the dictionary returned by the library.
        version = palworldInfo['version']
        palworldPlayers = palworldPlayers["players"]
        
        embed = discord.Embed(
            title=palworldOnlineTitle,
            color=blue,
        )

        embed.set_footer(text=time())

        embed.add_field(name="",value=f"{version}") 
        embed.add_field(name="",value=palworldAddress,inline=True)

        formattedUsernames = ""
        if len(palworldPlayers) > 0:
            embed.add_field(name="",value="",inline=False) 

            for i in palworldPlayers:
                formattedUsernames += " " + i['name'] + "\n"
            
            embed.add_field(name="Players", value="")
            embed.add_field(name="", value=formattedUsernames,inline=True)

    embed.set_footer(text=time())
    return embed

def format_minecraft(java, category, javaAddress, javaOnlineTitle="Minecraft", javaOfflineTitle="Minecraft: Offline"):
    """Formats the response of a minecraft server into a discord embed. When the server is offline, the 'java' paramater should be any type except for a string.

    Args:
        java (mcstatus.status_response.JavaStatusResponse): The response given from the mcstatus library. If the server is offline, or any error occured when contacting the server, this parameter should be anything but a string.
        category (str): The category used to locate the minecraft server.
        javaAddress (str): The server address to be displayed in the embed.
        javaOnlineTitle (str, optional): The title of the embed to be used when the server is online. Defaults to "Minecraft".
        javaOfflineTitle (str, optional): The title of the embed to be used when the server is offline. Defaults to "Minecraft: Offline".

    Returns:
        (discord.Embed): An embed that shows the server name, version, address, and online players.
    """
    
    embed = discord.Embed(
        title=javaOfflineTitle,
        color=red,
    )

    if type(java) != str:
        embed = discord.Embed(
        title=javaOnlineTitle,
        color=green,
        )

        javaVersion = java.version.name
        javaPlayerList = java.players.sample
            
        embed.add_field(name="", value=f"{javaVersion}")
        embed.add_field(name="", value=javaAddress,inline=True)

        if javaPlayerList != None:  
            formattedUsernames = ""

            for player in javaPlayerList:
                match(player.name):

                    case "ItsSquishy173": 
                        continue        
                        
                    case _:
                        formattedUsernames += " " + player.name + "\n"

                        embed.add_field(name="", value="",inline=False)
                        embed.add_field(name="Players", value="")
                        embed.add_field(name="", value=formattedUsernames,inline=True)

    embed.set_footer(text=time())
    return embed