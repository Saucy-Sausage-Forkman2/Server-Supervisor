from mcstatus import JavaServer
from mcstatus import BedrockServer
import math
import discord
import os
import asyncio
import json
from dotenv import load_dotenv
import asyncio
from palworld_api import PalworldAPI

from formatMinecraft import formatMinecraft
from scozFormatPalworld import scozFormatPalworld
from helpEmbed import help

load_dotenv()

address=os.getenv("address")
publicAddress=os.getenv("publicAddress")

scozJavaPort=os.getenv("scozJavaPort")
scozBedrockPort=os.getenv("scozBedrockPort")
scozPalworldRESTPort=os.getenv("scozPalworldRESTPort")
scozPalworldPort=os.getenv("scozPalworldPort")
dharMinecraftPort=os.getenv("dharMinecraftPort")

whitelisted = " (whitelisted)"

scozPalworldAddress=publicAddress+":"+scozPalworldPort+" (password protected)"
scozJavaAddress=publicAddress+":"+scozJavaPort+whitelisted
scozBedrockAddress=publicAddress+":"+scozBedrockPort+whitelisted
dharMinecraftAddress=publicAddress+":"+dharMinecraftPort+whitelisted

adminID=os.getenv("adminID")

#loads environment variables from the .env file to hide them from public code
#FILE MUST BE NAMED ".env"
prefix = '.'
   
#end of variable declaration
#------------------------------------------------------------------------
def openJson(name):
    if name[:-5] != ".json":
        return open(f"{name}.json","r")
    else:
        return open(f"{name}","r")

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

    await supervisorLoop(quickUpdate=True)

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

            del data[category][i][f'{message.channel.id}']
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

#minecraft-specific functions
async def minecraftPing(category):
    javaStatus = ""
    bedrockStatus = ""
    match(category):
        case "scoz":
            #Java Status Request
            try:
                javaStatus = await JavaServer.async_lookup(address+":"+scozJavaPort)
                javaStatus = await javaStatus.async_status()
            except:
                javaStatus = 0

            #Bedrock Status Request
            try:
                bedrockStatus = BedrockServer.lookup(address+":"+scozBedrockPort)
                bedrockStatus = await bedrockStatus.async_status()
            except:
                bedrockStatus = 0

            return formatMinecraft(javaStatus, category, scozJavaAddress, bedrockAddress=scozBedrockAddress, bedrock=bedrockStatus, bothOnlineTitle="Diesel Nation", onlyJavaTitle="Diesel Nation: Bedrock Unreachable", onlyBedrockTitle="Diesel Nation: Java Unreachable", bothOfflineTitle="Diesel Nation is Offline")

        case "dhar":
            #Java Status Request
            try:
            	javaStatus = await JavaServer.async_lookup(address+":"+dharMinecraftPort)
            	javaStatus = await javaStatus.async_status()
            except:
            	javaStatus = 0
            	
            return formatMinecraft(javaStatus, category, dharMinecraftAddress, onlyJavaTitle="Dharcraft 2077")


    #rewrite format functions into category independent versions
    
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Palworld-Specific Functions

async def palworldPing(category):
    match(category):
        case "scoz":
            username = os.getenv("SCOZPALWORLDADMINUSERNAME")
            password = os.getenv("SCOZPALWORLDADMINPASSWORD")
            api = PalworldAPI("http://"+address+":"+scozPalworldRESTPort, username, password)

            server_info = await api.get_server_info() #dictionary, not json
            palworldPlayers = await api.get_player_list()# print all names in array again
            palworldSettings = await api.get_server_settings()

            return scozFormatPalworld(server_info,palworldSettings,palworldPlayers,scozPalworldAddress)

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await supervisorLoop()

#------------------------------------------------------------------------

@client.event
async def on_message(message):
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
                    #dontcrash = await client.fetch_channel(f'{i}')
                    #print(f'Updating supervisor in {dontcrash}')
                    #dontcrash = await dontcrash.fetch_message(data[f'{i}'])
                    #dontcrash = await dontcrash.edit(content=None, embeds=ping)
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

        if quickUpdate: return
        await asyncio.sleep(delayInSeconds)

#------------------------------------------------------------------------

client.run(os.getenv('TOKEN'))
