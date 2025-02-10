import discord
import json
import asyncio

from JsonInterpreter import json_create_supervisor, json_remove_supervisor, json_open, json_write
from ServerPingFunctions import ark_ping, minecraft_ping, palworld_ping

async def supervisor_loop(client, quickUpdate=False, updateDelayInSeconds=60):
    """Infinite loop that updates all supervisors. Does not return.

    Args:
        client (discord.Client): The bot client used to lookup messages and channels by their numerical id.
        quickUpdate (bool, optional): If true, will only run once. Defaults to False.
        updateDelayInSeconds (int, optional): How long to sleep between each iteration of the loop. Defaults to 60.
    """
    
    while True:
        jsonFile = json_open()
        jsonFile = json.load(jsonFile)

        minecraftStatus = 0
        palworldStatus = 0

        for jsonCategory in jsonFile:
            match(jsonCategory):

                case "scoz":
                    minecraftStatus = await minecraft_ping(category="scoz")
                    palworldStatus = await palworld_ping(category="scoz")
                    ping = [minecraftStatus,palworldStatus]
                    
                    for jsonGuild in range( len( jsonFile[jsonCategory])):
                        for jsonChannel in jsonFile[jsonCategory][jsonGuild]:

                            supervisorChannel = await client.fetch_channel(f'{jsonChannel}')
                            supervisorMessage = await supervisorChannel.fetch_message(jsonFile[jsonCategory][jsonGuild][jsonChannel])
                            await supervisorMessage.edit(content=None, embeds=ping)

                case "dhar":
                    minecraftStatus = await minecraft_ping(category="dhar")
                
                    for jsonGuild in range( len( jsonFile[jsonCategory])):
                        for jsonChannel in jsonFile[jsonCategory][jsonGuild]:

                            supervisorChannel = await client.fetch_channel(f'{jsonChannel}')
                            supervisorMessage = await supervisorChannel.fetch_message(jsonFile[jsonCategory][jsonGuild][jsonChannel])
                            await supervisorMessage.edit(content=None, embed=minecraftStatus)

                case "dwarf":
                    arkStatus = await ark_ping("dwarf")

                    for jsonGuild in range( len( jsonFile[jsonCategory])):
                        for jsonChannel in jsonFile[jsonCategory][jsonGuild]:

                            supervisorChannel = await client.fetch_channel(f'{jsonChannel}')
                            supervisorMessage = await supervisorChannel.fetch_message(jsonFile[jsonCategory][jsonGuild][jsonChannel])
                            await supervisorMessage.edit(content=None, embed=arkStatus)

        if quickUpdate: return
        await asyncio.sleep(updateDelayInSeconds)