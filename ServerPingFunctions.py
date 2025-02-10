import os
import discord
from mcstatus import JavaServer
from mcstatus import BedrockServer
import a2s
from dotenv import load_dotenv

from ResponseFormatFunctions import format_ark, format_minecraft, format_palworld

load_dotenv()

ADDRESS=os.getenv("ADDRESS")
ADDRESS_2=os.getenv("ADDRESS_2")
SCOZ_PUBLIC_ADDRESS=os.getenv("SCOZ_PUBLIC_ADDRESS")
DHAR_PUBLIC_ADDRESS=os.getenv("DHAR_PUBLIC_ADDRESS")

SCOZ_JAVA_PORT=os.getenv("SCOZ_JAVA_PORT")
SCOZ_BEDROCK_PORT=os.getenv("SCOZ_BEDROCK_PORT")
SCOZ_PALWORLD_PORT=os.getenv("SCOZ_PALWORLD_PORT")
DHAR_MINECRAFT_PORT=os.getenv("DHAR_MINECRAFT_PORT")

MINECRAFT_SUB_DOMAIN="mc."

SCOZ_PALWORLD_ADDRESS=SCOZ_PUBLIC_ADDRESS+":"+SCOZ_PALWORLD_PORT
SCOZ_JAVA_ADDRESS=MINECRAFT_SUB_DOMAIN+SCOZ_PUBLIC_ADDRESS
DHAR_MINECRAFT_ADDRESS=MINECRAFT_SUB_DOMAIN+DHAR_PUBLIC_ADDRESS

arkPortsToQuery = [7011]

async def minecraft_ping(category):
    javaStatus = ""
    bedrockStatus = ""

    match(category):
        case "scoz":
            try:
                javaStatus = await JavaServer.async_lookup(ADDRESS+":"+SCOZ_JAVA_PORT)
                javaStatus = await javaStatus.async_status()

            except Exception as e:
                javaStatus = e

            return format_minecraft(
                javaStatus, 
                category, 
                SCOZ_JAVA_ADDRESS, 
                javaOnlineTitle="Bellycraft - Java and Bedrock", 
                javaOfflineTitle="Bellycraft Offline")

        case "dhar":
            #Java Status Request
            try:
            	javaStatus = await JavaServer.async_lookup(ADDRESS_2+":"+DHAR_MINECRAFT_PORT)
            	javaStatus = await javaStatus.async_status()

            except Exception as e:
            	javaStatus = e

            return format_minecraft(
                javaStatus, 
                category, 
                DHAR_MINECRAFT_ADDRESS, 
                javaOnlineTitle="Mexican Border RP 2: Dhar Harder")

async def palworld_ping(category):
    match(category):
        case "scoz":
            try:
                palworldAddressTuple = (ADDRESS_2, SCOZ_PALWORLD_PORT)

                palworldPlayers = await a2s.aplayers(palworldAddressTuple)
                palworldInfo = await a2s.aplayers(palworldAddressTuple)

                return format_palworld(palworldInfo, palworldPlayers, SCOZ_PALWORLD_ADDRESS)

            except Exception as e:
                return format_palworld(1,1,SCOZ_PALWORLD_ADDRESS)

async def ark_ping(category):
    match(category):
        case "dwarf":
            arkServerCount = len(arkPortsToQuery)
            arkServerQuery2DArray = [] 

            for arkPort in arkPortsToQuery:
                try:
                    arkAddress = (ADDRESS_2,arkPort)

                    arkServerInfo = await a2s.ainfo(arkAddress)
                    arkServerPlayers = await a2s.aplayers(arkAddress)

                    arkServerQuery2DArray.append([arkAddress,arkServerInfo,arkServerPlayers])

                except Exception as e:
                    arkServerQuery2DArray.append(e)

            return format_ark(arkServerQuery2DArray)