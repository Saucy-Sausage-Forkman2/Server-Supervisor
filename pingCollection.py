import os
import discord
from mcstatus import JavaServer
from mcstatus import BedrockServer
from palworld_api import PalworldAPI
import a2s
from formatMinecraft import formatMinecraft
from scozFormatPalworld import scozFormatPalworld
from formatArk import formatArk

from dotenv import load_dotenv

load_dotenv()

address=os.getenv("address")
address2=os.getenv("address2")
scozPublicAddress=os.getenv("scozPublicAddress")
dharPublicAddress=os.getenv("dharPublicAddress")

scozJavaPort=os.getenv("scozJavaPort")
scozBedrockPort=os.getenv("scozBedrockPort")
scozPalworldRESTPort=os.getenv("scozPalworldRESTPort")
scozPalworldPort=os.getenv("scozPalworldPort")
dharMinecraftPort=os.getenv("dharMinecraftPort")

whitelisted = " (whitelisted)"

minecraftSubDomain="mc."

scozPalworldAddress=scozPublicAddress+":"+scozPalworldPort+" (password protected)"
scozJavaAddress=minecraftSubDomain+scozPublicAddress+whitelisted
scozBedrockAddress=minecraftSubDomain+scozPublicAddress+whitelisted
dharMinecraftAddress=minecraftSubDomain+dharPublicAddress+whitelisted

adminID=os.getenv("adminID")

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

            return formatMinecraft(javaStatus, 
                category, 
                scozJavaAddress, 
                bedrockAddress=scozBedrockAddress,
                bedrock=bedrockStatus, 
                bothOnlineTitle="Bellycraft", 
                onlyJavaTitle="Bellycraft: Bedrock Unreachable", 
                onlyBedrockTitle="Bellycraft: Java Unreachable", 
                bothOfflineTitle="Bellycraft Offline")

        case "dhar":
            #Java Status Request
            try:
            	javaStatus = await JavaServer.async_lookup(address2+":"+dharMinecraftPort)
            	javaStatus = await javaStatus.async_status()
            except Exception as e:
            	print(e)
            	javaStatus = 0

            	
            return formatMinecraft(javaStatus, category, dharMinecraftAddress, onlyJavaTitle="Mexican Border RP 2: Dhar Harder")

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Palworld-Specific Functions

async def palworldPing(category):
    match(category):
        case "scoz":
            username = os.getenv("SCOZPALWORLDADMINUSERNAME")
            password = os.getenv("SCOZPALWORLDADMINPASSWORD")
            api = PalworldAPI("http://"+address2+":"+scozPalworldRESTPort, username, password)
            
            server_info = await api.get_server_info() #dictionary, not json
            palworldPlayers = await api.get_player_list()# print all names in array again
            palworldSettings = await api.get_server_settings()

            return scozFormatPalworld(server_info,palworldSettings,palworldPlayers,scozPalworldAddress)

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Ark-specific functions

async def arkPing(category):
    match(category):
        case "dwarf":
            arkPortsToQuery = [7011]
            arkServerCount = len(arkPortsToQuery)
            #player = a2s.players(arkAddress)[0]
            #print(f"{player.name}, {math.trunc(player.duration/60)} minutes")
            #address, serverInfo, serverPlayers
            arkServerQuery2DArray = [] 
            for arkPort in arkPortsToQuery:
                try:
                    arkAddress = (address2,arkPort)
                    arkServerInfo = await a2s.ainfo(arkAddress)
                    arkServerPlayers = await a2s.aplayers(arkAddress)
                    arkServerQuery2DArray.append([arkAddress,arkServerInfo,arkServerPlayers])
                except Exception as e:
                    print(e)
                    continue
            return await formatArk(arkServerQuery2DArray)
                
            
        

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
