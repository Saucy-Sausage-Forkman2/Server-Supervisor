import os
import discord
from mcstatus import JavaServer
from mcstatus import BedrockServer
from palworld_api import PalworldAPI
import a2s
from FormatMinecraft import format_minecraft
from ScozFormatPalworld import scoz_format_palworld
from FormatArk import format_ark

from dotenv import load_dotenv

load_dotenv()

ADDRESS=os.getenv("ADDRESS")
ADDRESS_2=os.getenv("ADDRESS_2")
SCOZ_PUBLIC_ADDRESS=os.getenv("SCOZ_PUBLIC_ADDRESS")
DHAR_PUBLIC_ADDRESS=os.getenv("DHAR_PUBLIC_ADDRESS")

SCOZ_JAVA_PORT=os.getenv("SCOZ_JAVA_PORT")
SCOZ_BEDROCK_PORT=os.getenv("SCOZ_BEDROCK_PORT")
SCOZ_PALWORLD_REST_PORT=os.getenv("SCOZ_PALWORLD_REST_PORT")
SCOZ_PALWORLD_PORT=os.getenv("SCOZ_PALWORLD_PORT")
DHAR_MINECRAFT_PORT=os.getenv("DHAR_MINECRAFT_PORT")

SCOZ_PALWORLD_ADMIN_USERNAME = os.getenv("SCOZ_PALWORLD_ADMIN_USERNAME")
SCOZ_PALWORLD_ADMIN_PASSWORD = os.getenv("SCOZ_PALWORLD_ADMIN_PASSWORD")

MINECRAFT_SUB_DOMAIN="mc."

SCOZ_PALWORLD_ADDRESS=SCOZ_PUBLIC_ADDRESS+":"+SCOZ_PALWORLD_PORT
SCOZ_JAVA_ADDRESS=MINECRAFT_SUB_DOMAIN+SCOZ_PUBLIC_ADDRESS
SCOZ_BEDROCK_ADDRESS=MINECRAFT_SUB_DOMAIN+SCOZ_PUBLIC_ADDRESS
DHAR_MINECRAFT_ADDRESS=MINECRAFT_SUB_DOMAIN+DHAR_PUBLIC_ADDRESS

ADMIN_ID=os.getenv("ADMIN_ID")

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#minecraft-specific functions

async def minecraft_ping(category):
    javaStatus = ""
    bedrockStatus = ""
    match(category):
        case "scoz":
            #Java Status Request
            try:
                javaStatus = await JavaServer.async_lookup(ADDRESS+":"+SCOZ_JAVA_PORT)
                javaStatus = await javaStatus.async_status()
            except:
                javaStatus = 0

            #Bedrock Status Request
            try:
                bedrockStatus = BedrockServer.lookup(ADDRESS+":"+SCOZ_BEDROCK_PORT)
                bedrockStatus = await bedrockStatus.async_status()
            except:
                bedrockStatus = 0

            return format_minecraft(javaStatus, 
                category, 
                SCOZ_JAVA_ADDRESS, 
                bedrockAddress=SCOZ_BEDROCK_ADDRESS,
                bedrock=bedrockStatus, 
                bothOnlineTitle="Bellycraft", 
                onlyJavaTitle="Bellycraft: Bedrock Unreachable", 
                onlyBedrockTitle="Bellycraft: Java Unreachable", 
                bothOfflineTitle="Bellycraft Offline")

        case "dhar":
            #Java Status Request
            try:
            	javaStatus = await JavaServer.async_lookup(ADDRESS_2+":"+DHAR_MINECRAFT_PORT)
            	javaStatus = await javaStatus.async_status()
            except Exception as e:
            	print(e)
            	javaStatus = 0

            	
            return format_minecraft(javaStatus, category, DHAR_MINECRAFT_ADDRESS, onlyJavaTitle="Mexican Border RP 2: Dhar Harder")

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Palworld-Specific Functions

async def palworld_ping(category):
    match(category):
        case "scoz":
            api = PalworldAPI("http://"+ADDRESS_2+":"+SCOZ_PALWORLD_REST_PORT, SCOZ_PALWORLD_ADMIN_USERNAME, SCOZ_PALWORLD_ADMIN_PASSWORD)
            
            server_info = await api.get_server_info() #dictionary, not json
            palworldPlayers = await api.get_player_list()# print all names in array again
            palworldSettings = await api.get_server_settings()

            return scoz_format_palworld(server_info,palworldSettings,palworldPlayers,SCOZ_PALWORLD_ADDRESS)

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Ark-specific functions

async def ark_ping(category):
    match(category):
        case "dwarf":
            arkPortsToQuery = [7011]
            arkServerCount = len(arkPortsToQuery)
            #player = a2s.players(arkAddress)[0]
            #print(f"{player.name}, {math.trunc(player.duration/60)} minutes")
            #ADDRESS, serverInfo, serverPlayers
            arkServerQuery2DArray = [] 
            for arkPort in arkPortsToQuery:
                try:
                    arkAddress = (ADDRESS_2,arkPort)
                    arkServerInfo = await a2s.ainfo(arkAddress)
                    arkServerPlayers = await a2s.aplayers(arkAddress)
                    arkServerQuery2DArray.append([arkAddress,arkServerInfo,arkServerPlayers])
                except Exception as e:
                    print(e)
                    continue
            return await format_ark(arkServerQuery2DArray)
                
            
        

#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
