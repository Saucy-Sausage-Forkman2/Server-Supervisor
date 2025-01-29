import math
import discord
import os
import asyncio
import json
import asyncio
import a2s

from HelpEmbed import generate_help_embed
from PingCollection import minecraft_ping,palworld_ping,ark_ping


ADMIN_ID=os.getenv("ADMIN_ID")

jsonFileName="StatusMessages"

#loads environment variables from the .env file to hide them from public code
#FILE MUST BE NAMED ".env"

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
def open_json(name):
    if name[:-5] != ".json":
        return open(f"{name}.json","r")
    else:
        return open(f"{name}","r")

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

def write_json(data, name):
    if name[:-5] != ".json":
        with open(f"{name}.json","r+") as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(data, json_file, indent=4)
            json_file.close()
        return
    else:
        with open(f"{name}","r+") as json_file:
            json_file.seek(0)
            json_file.truncate()
            json.dump(data, json_file, indent=4)
            json_file.close()
        return

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

async def json_create_supervisor(message, category):
    category = f"{category}"
    pendingMessage = await message.channel.send("Pinging...")

    try:
        await json_remove_supervisor(message,category,shouldPrint=False)
    except Exception as e: print(e)
        
    json_file = open_json(jsonFileName)
    data = json.load(json_file)

    data[category].append({pendingMessage.channel.id:pendingMessage.id})
    write_json(data,jsonFileName)
    print(data)
    await supervisor_loop(quickUpdate=True)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

async def json_remove_supervisor(message, category,shouldPrint=True):
    category = f"{category}"

    json_file = open_json(jsonFileName)
    data = json.load(json_file)

    for i in range(len(data[category])):
        try:

            try:
                dontcrash = await client.fetch_channel(message.channel.id)
                dontcrash = await dontcrash.fetch_message(data[category][i][f"{message.channel.id}"])
                await dontcrash.delete()
            except Exception as e: 
                print(e)

            del data[category][i]
        except Exception as e: 
            print(e)
            continue
        else:
            #The strategy of using seek(0) to overwrite a file only works if the new text is equally long or longer than what already exists, otherwise
            #the difference will be appended to the end of the file. The solution is to truncate it from the beginning, effectively erasing it.
            write_json(data,jsonFileName)
            if shouldPrint: await message.channel.send("Supervisor disabled.")
            return
    if shouldPrint: await message.channel.send("There is no active supervisor in this channel.")
    return
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
async def supervisor_loop(quickUpdate=False):
    delayInSeconds = 60
    while True:
        json_file = open_json(jsonFileName)
        data = json.load(json_file)

        minecraftStatus = 0
        palworldStatus = 0

        for i in data:
            match(i):
                case "scoz":
                    minecraftStatus = await minecraft_ping(category="scoz")
                    palworldStatus = await palworld_ping(category="scoz")
                    ping = [minecraftStatus,palworldStatus]
                    for j in range( len( data[i])):
                        for k in data[i][j]:
                            #don't like the nesting, but this is the easiest way to get the channel IDs from the json array
                            supervisorChannel = await client.fetch_channel(f'{k}')
                            supervisorMessage = await supervisorChannel.fetch_message(data[i][j][k])
                            await supervisorMessage.edit(content=None, embeds=ping)
                case "dhar":
                    minecraftStatus = await minecraft_ping(category="dhar")
                
                    for j in range( len( data[i])):
                        for k in data[i][j]:
                            #copy and paste saves lives
                            supervisorChannel = await client.fetch_channel(f'{k}')
                            supervisorMessage = await supervisorChannel.fetch_message(data[i][j][k])
                            await supervisorMessage.edit(content=None, embed=minecraftStatus)
                case "dwarf":
                    arkStatus = await ark_ping("dwarf")
                    for j in range( len( data[i])):
                        for k in data[i][j]:
                            #copy and paste saves lives
                            supervisorChannel = await client.fetch_channel(f'{k}')
                            supervisorMessage = await supervisorChannel.fetch_message(data[i][j][k])
                            await supervisorMessage.edit(content=None, embed=arkStatus)

        if quickUpdate: return
        await asyncio.sleep(delayInSeconds)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

prefix = '.'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await supervisor_loop()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


@client.event
async def on_message(message):
    if not message.content.startswith(prefix) and message.author.id != ADMIN_ID:
        return
    
    arguments = message.content[1:].split(" ")
    command = arguments.pop(0)
    if len(arguments) > 0:
        argumentRaw = message.content[1:].split(" ", 1)[1]  

    match command:
        case "create":
            if len(arguments) < 2:
                await message.channel.send("Please provide a category.")
                return
            match(arguments[0]):
                case "supervisor":
                    await json_create_supervisor(message, arguments[1])

                case _:
                    await message.channel.send(embed=generate_help_embed())

        case "delete":
            if len(arguments) < 2:
                await message.channel.send("Please provide a category.")
                return  
            match(arguments[0]):
                case "supervisor":
                    await json_remove_supervisor(message, arguments[1])

                case _:
                    await message.channel.send(embed=generate_help_embed())

        case _:
            await message.channel.send(embed=generate_help_embed())
                

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------



client.run(os.getenv('TOKEN'))







