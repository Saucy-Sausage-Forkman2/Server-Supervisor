import asyncio
import discord
import json
import os
import datetime

def time():
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
    red = discord.Colour.red()
    green = discord.Colour.green()
    arkFormattedPlayers = ""
    embed = 0
    
    arkEmbedFields = []

    #if there was an error, we should make an exception and skip code
    if arkServerQuery2DArray == []:
        embed = discord.Embed(
            title=arkAllServersOfflineTitle,
            color=red
            )

        #otherwise, create and format the embed.
    else:
        
        for arkServerInfoArray in arkServerQuery2DArray:
            #0 address, 1 serverInfo, 2 serverPlayers
            arkServerInfo = arkServerInfoArray[1]

            arkServerName = arkServerInfo.server_name
            arkMapName = arkServerInfo.map_name
            arkPlayerCount = arkServerInfo.player_count

            #formatting username text, if there are players online
            for player in arkServerInfoArray[2]:
                arkFormattedPlayers += " " + player.name + ","
            arkFormattedPlayers=arkFormattedPlayers[:-1]
            
            #arkServerName is cut twelve short to remove version number
            match(arkServerName):
                case "TheIsland":
                    arkServerName="The Island"
            arkEmbedFieldTemplate = f"{arkServerName[:-12]} ({arkMapName}): {arkPlayerCount}"
            arkEmbedFields.append([arkEmbedFieldTemplate,arkFormattedPlayers])

        embed = discord.Embed(
            title=arkAllServersOnlineTitle,
            color=green)
        for arkEmbedPair in arkEmbedFields:
            embed.add_field(name=arkEmbedPair[0],value=arkEmbedPair[1])

        
    embed.set_footer(text=time())
    return embed

def scoz_format_palworld(server_info,palworldSettings,palworldPlayers,scozPalworldAddress):
    palworldTitle = "Bellyworld"	
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

def format_minecraft(java, category, javaAddress, bedrockAddress=None, bedrock=None, bothOnlineTitle="Minecraft Server", onlyJavaTitle="Bedrock Unreachable", onlyBedrockTitle="Java Unreachable", bothOfflineTitle="Minecraft Offline"):
    zeroServerColor = discord.Colour.red()
    oneServerColor = discord.Colour.yellow()
    twoServerColor = discord.Colour.green()

    embed = 0
    if bedrock != None and bedrockAddress != None:
    #both java and bedrock
        if java != 0 and bedrock != 0:
            embed = discord.Embed(
                title=bothOnlineTitle,
                color=twoServerColor,
            )
        #---------------------------------
        #only java, no bedrock
        elif java != 0 and bedrock == 0:
            embed = discord.Embed(
                title=onlyJavaTitle,
                color=oneServerColor,
            )
        #---------------------------------
        #only bedrock, no java
        elif java == 0 and bedrock != 0:
            embed = discord.Embed(
                title=onlyBedrockTitle,
                color=oneServerColor,
            )
            embed.add_field(name="Java", value="",inline=False)
        #---------------------------------
        #neither bedrock or java
        elif java == 0 and bedrock == 0:
            embed = discord.Embed(
                title=bothOfflineTitle,
                color=zeroServerColor,
            )

            embed.set_footer(text=time())

            #We can take a shortcut here since there is no other data to add
            embed.add_field(name="Java", value="Offline")
            embed.add_field(name="",value="",inline=False) # a new line to separate the player fields so it looks nice
            embed.add_field(name="Bedrock", value="Offline")

            return embed
            
        #---------------------------------
        formattedUsernames = ""
        for player in javaPlayerList:
            formattedUsernames += " " + player.name + "\n"
            
        #if java is online
        if java != 0:
            #if the server is alive
            version = java.version.name
            players = java.players.online
            maxPlayers=java.players.max
            javaPlayerList = java.players.sample
            #only java servers provide a list of active players

            accountsToHide = 0
            #go through the array of usernames and compile them into a list for beauty
            formattedUsernames = ""
            if javaPlayerList != None:
                for player in javaPlayerList:
                    match(player.name):
                        case "ItsSquishy173": 
                            accountsToHide += 1
                            continue               
                        case _:
                            formattedUsernames += " " + i.name + "\n"
            embed.add_field(name="Players", value=f"{players - accountsToHide}" + "/" + f"{maxPlayers}")
            embed.add_field(name="", value=formattedUsernames,inline=True)

            embed.add_field(name="", value="",inline=False)

            #I placed the player count before the Java server header as it applies to both java and bedrock, and it feels wrong to have the
            #player count only under one or under both. And it has to be exist.
            embed.add_field(name="Java", value=f"{version}")
            #Putting the game version first as it's the most important for new players, and is important in general
        else:
            embed.add_field(name="",value="Server Offline")
        
        #if bedrock is online
        if bedrock != 0:
            version = bedrock.version.name
            embed.add_field(name="Bedrock", value=f"{version}")
            embed.add_field(name="",value=bedrockAddress,inline=False)
        else:
            embed.add_field(name="Bedrock",value="Server Offline")

        embed.set_footer(text=time())
        return embed
    
    #if there is only a java server
    if java != 0:
        embed = discord.Embed(
            title=onlyJavaTitle,
            color=twoServerColor,
        )

        version = java.version.name
        players = java.players.online
        maxPlayers=java.players.max
        javaPlayerList = java.players.sample

        embed.add_field(name="Players", value=f"{players}" + "/" + f"{maxPlayers}")

        if javaPlayerList != None:
            embed.add_field(name="", value=formattedUsernames,inline=True)
        else: embed.add_field(name="",value="",inline=True) # a new line to separate the player fields so it looks nice
        
        embed.add_field(name="", value="",inline=False)

        #I placed the player count before the Java server header as it applies to both java and bedrock, and it feels wrong to have the
        #player count only under one or under both. And it has to be exist.
        embed.add_field(name="Java", value="",inline=True)
        #Putting the game version first as it's the most important for new players, and is important in general
        embed.add_field(name="", value=f"{version}")

        #The java server has more details since both servers run hand in hand, so having all information about both is simply redundant.
        embed.add_field(name="",value=javaAddress,inline=False)
        embed.set_footer(text=time())

        return embed
        
    else:
        embed = discord.Embed(
            title=onlyJavaTitle,
            color=zeroServerColor,
        )

        embed.add_field(name="",value="Server Offline")
        embed.set_footer(text=time())
        
        return embed