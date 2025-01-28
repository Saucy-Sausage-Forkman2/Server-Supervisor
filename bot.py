import math
import discord
import os
import asyncio
import json
import asyncio
import a2s

from helpEmbed import help
from pingCollection import minecraftPing,palworldPing,arkPing



#loads environment variables from the .env file to hide them from public code
#FILE MUST BE NAMED ".env"

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
def openJson(name):
    if name[:-5] != ".json":
        return open(f"{name}.json","r")
    else:
        return open(f"{name}","r")

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

def writeJson(data, name):
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

async def jsonCreateSupervisor(message, category):
    category = f"{category}"
    pendingMessage = await message.channel.send("Pinging...")

    try:
        await jsonRemoveSupervisor(message,category,shouldPrint=False)
    except Exception as e: print(e)
        
    json_file = openJson("status_messages")
    data = json.load(json_file)

    data[category].append({pendingMessage.channel.id:pendingMessage.id})
    writeJson(data,"status_messages")
    print(data)
    await supervisorLoop(quickUpdate=True)

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

async def jsonRemoveSupervisor(message, category,shouldPrint=True):
    category = f"{category}"

    json_file = openJson("status_messages")
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
            writeJson(data,"status_messages")
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
async def supervisorLoop(quickUpdate=False):
    delayInSeconds = 60
    while True:
        json_file = openJson("status_messages")
        data = json.load(json_file)

        minecraftStatus = 0
        palworldStatus = 0

        for i in data:
            match(i):
                case "scoz":
                    minecraftStatus = await minecraftPing(category="scoz")
                    palworldStatus = await palworldPing(category="scoz")
                    ping = [minecraftStatus,palworldStatus]
                    for j in range( len( data[i])):
                        for k in data[i][j]:
                            #don't like the nesting, but this is the easiest way to get the channel IDs from the json array
                            supervisorChannel = await client.fetch_channel(f'{k}')
                            supervisorMessage = await supervisorChannel.fetch_message(data[i][j][k])
                            await supervisorMessage.edit(content=None, embeds=ping)
                case "dhar":
                    minecraftStatus = await minecraftPing(category="dhar")
                
                    for j in range( len( data[i])):
                        for k in data[i][j]:
                            #copy and paste saves lives
                            supervisorChannel = await client.fetch_channel(f'{k}')
                            supervisorMessage = await supervisorChannel.fetch_message(data[i][j][k])
                            await supervisorMessage.edit(content=None, embed=minecraftStatus)
                case "dwarf":
                    arkStatus = await arkPing("dwarf")
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
    await supervisorLoop()

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


@client.event
async def on_message(message):
    print("s")
    if not message.content.startswith(prefix) and message.author != adminID:
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
                    await jsonCreateSupervisor(message, arguments[1])

                case _:
                    await message.channel.send(embed=help())

        case "delete":
            if len(arguments) < 2:
                await message.channel.send("Please provide a category.")
                return  
            match(arguments[0]):
                case "supervisor":
                    await jsonRemoveSupervisor(message, arguments[1])

                case _:
                    await message.channel.send(embed=help())

        case _:
            await message.channel.send(embed=help())
                

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------



client.run(os.getenv('TOKEN'))







