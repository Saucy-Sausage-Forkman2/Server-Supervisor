import json
import discord
from dotenv import load_dotenv
from getTimestamp import time
def scozFormatPalworld(server_info,palworldSettings,palworldPlayers,scozPalworldAddress):
    palworldTitle = "Palworld: Hawk Tuah the Tower"	
    aliveColor = discord.Colour.blue()
    deadColor = discord.Colour.dark_red()
    try:   
        #If the palworld server is down, the library will return a dictionary with the single entry of 'error'. In this case, we check to see if the dictionary contains
        # any key for error. If it does, that means the server is inaccessible.
        # However, in that case, there would be no exception. So the code looks a little funny, if not messy. But that's the price to pay for my approach.
        if server_info['error']:
            pass

    except:
        #this runs if there is no error, both in connecting to the server and in the dictionary returned by the library.
        palworldSettings = json.loads(palworldSettings)
        palworldPlayers = palworldPlayers["players"]
        version = server_info['version']
        #myDescription=server_info['servername']
        maxPlayers = palworldSettings["ServerPlayerMaxNum"]
        playerCount = len(palworldPlayers)
        
        embed = discord.Embed(
        title=palworldTitle,
        color=aliveColor,
        #description=myDescription
        )

        embed.set_footer(text=time())

        embed.add_field(name="Version",value="",inline=True) 
        embed.add_field(name="",value=f"{version}",inline=True) 
        embed.add_field(name="",value="",inline=False) 
        embed.add_field(name="Players", value=f"{playerCount}" + "/" + f"{maxPlayers}",inline=True)

        formattedUsernames = ""
        for i in palworldPlayers:
            formattedUsernames += " " + i['name'] + "\n"
        embed.add_field(name="", value=formattedUsernames,inline=True)
        embed.add_field(name="",value=scozPalworldAddress,inline=False)

    else:
        embed = discord.Embed(
        title=palworldTitle,
        color=deadColor,
        description="The Server is Offline."
        )

        embed.set_footer(text=time())

    return embed
