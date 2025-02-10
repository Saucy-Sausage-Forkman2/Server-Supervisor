import os
import discord
from mcstatus import JavaServer
from mcstatus import BedrockServer
import a2s
from dotenv import load_dotenv
from palworld_api import PalworldAPI

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

SCOZ_PALWORLD_REST_PORT=os.getenv("SCOZ_PALWORLD_REST_PORT")
SCOZ_PALWORLD_ADMIN_USERNAME = os.getenv("SCOZ_PALWORLD_ADMIN_USERNAME")
SCOZ_PALWORLD_ADMIN_PASSWORD = os.getenv("SCOZ_PALWORLD_ADMIN_PASSWORD")

SCOZ_PALWORLD_ADDRESS=SCOZ_PUBLIC_ADDRESS+":"+SCOZ_PALWORLD_PORT
SCOZ_JAVA_ADDRESS=MINECRAFT_SUB_DOMAIN+SCOZ_PUBLIC_ADDRESS
DHAR_MINECRAFT_ADDRESS=MINECRAFT_SUB_DOMAIN+DHAR_PUBLIC_ADDRESS
arkPortToAddressConversionArray = ["theisland.bellycraft.net", "aberration.bellycraft.net", "extinction.bellycraft.net"]
arkPortToMapConversionArray     = ["The Island"              , "Aberration"               , "Extinction"]
arkPortsToQuery                 = [7001                      , 7004                       ,  7007]

async def minecraft_ping(category):
    """Contacts the Minecraft server of the given category, and returns a discord embed.

    Args:
        category (str): The category to use when locating the Minecraft server.

    Returns:
        (discord.Embed): An embed that shows the server name, version, address, and online players.
    """

    javaStatus = ""
    bedrockStatus = ""

    match(category):
        case "scoz":
            try:
                javaStatus = await JavaServer.async_lookup(ADDRESS+":"+SCOZ_JAVA_PORT)
                javaStatus = await javaStatus.async_status()

            except Exception as e:
                javaStatus = f"{e}"

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
            	javaStatus = f"{e}"

            return format_minecraft(
                javaStatus, 
                category, 
                DHAR_MINECRAFT_ADDRESS, 
                javaOnlineTitle="Mexican Border RP 2: Dhar Harder")

async def palworld_ping(category):
    """Contacts the Palworld server of the given category, and returns a discord embed.

    Args:
        category (str): The category to use when locating the Palworld server.

    Returns:
        (discord.Embed): An embed that shows the server name, version, address, and online players.
    """

    match(category):
        case "scoz":
            api = PalworldAPI("http://"+ADDRESS_2+":"+SCOZ_PALWORLD_REST_PORT, SCOZ_PALWORLD_ADMIN_USERNAME, SCOZ_PALWORLD_ADMIN_PASSWORD)

            palworldInfo = await api.get_server_info() #dictionary, not json
            palworldPlayers = await api.get_player_list()# print all names in array again
            return format_palworld(palworldInfo, palworldPlayers, SCOZ_PALWORLD_ADDRESS)

async def ark_ping(category):
    """Contacts the entire Ark Survival Evolved server cluster of the given category, and returns a discord embed.

    Args:
        category (str): The category to use when locating the Ark cluster.

    Returns:
        (discord.Embed): An embed that shows the server names, addresses, and the number of online players in each server.
    """

    match(category):
        case "dwarf":
            arkServerCount = len(arkPortsToQuery)
            arkServerQuery2DArray = [] 

            for arkPortIndex in range(len(arkPortsToQuery)):
                arkMapName = arkPortToMapConversionArray[arkPortIndex]
                arkAddress = (ADDRESS_2,arkPortsToQuery[arkPortIndex])
                
                try:
                    arkServerInfo = await a2s.ainfo(arkAddress)
                    arkServerPlayers = await a2s.aplayers(arkAddress)

                    arkServerQuery2DArray.append([arkPortToAddressConversionArray[arkPortIndex],arkServerInfo,arkServerPlayers, arkMapName])

                except Exception as e:
                    print(e)
                    arkServerQuery2DArray.append(f"{arkMapName}: Offline")
                    continue

            return format_ark(arkServerQuery2DArray)
