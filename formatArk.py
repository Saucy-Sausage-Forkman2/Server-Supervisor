import asyncio
import discord
from getTimestamp import time

async def formatArk(arkServerQuery2DArray, arkAllServersOfflineTitle="Ark: Offline",arkAllServersOnlineTitle="Ark"):
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
            #Somehow cleanly format all of these values into one or two fields in the embed, NOT one embed per server!

            arkServerName = arkServerInfo.server_name
            arkMapName = arkServerInfo.map_name
            arkPlayerCount = arkServerInfo.player_count
            arkMaxPlayers = arkServerInfo.max_players

            #formatting username text, if there are players online
            for player in arkServerInfoArray[2]:
                arkFormattedPlayers += " " + player.name + ","
            arkFormattedPlayers=arkFormattedPlayers[:-1]
            #arkServerName is cut twelve short to remove version number
            match(arkServerName):
                case "TheIsland":
                    arkServerName="The Island"
            arkEmbedFieldTemplate = f"{arkServerName[:-12]} ({arkMapName}): {arkPlayerCount}/{arkMaxPlayers}"
            arkEmbedFields.append([arkEmbedFieldTemplate,arkFormattedPlayers])

        embed = discord.Embed(
            title=arkAllServersOnlineTitle,
            color=green)
        for arkEmbedPair in arkEmbedFields:
            embed.add_field(name=arkEmbedPair[0],value=arkEmbedPair[1])

        
    embed.set_footer(text=time())
    return embed




















#Documentation for a2s
"""
protocol: int
    Protocol version used by the server

    server_name: StrType
    Display name of the server

    map_name: StrType
    The currently loaded map

    folder: StrType
    Name of the game directory

    game: StrType
    Name of the game

    app_id: int
    App ID of the game required to connect

    player_count: int
    Number of players currently connected

    max_players: int
    Number of player slots available

    bot_count: int
    Number of bots on the server

    server_type: StrType
    Type of the server:
    'd': Dedicated server
    'l': Non-dedicated server
    'p': SourceTV relay (proxy)

    platform: StrType
    Operating system of the server
    'l', 'w', 'm' for Linux, Windows, macOS

    password_protected: bool
    Server requires a password to connect

    vac_enabled: bool
    Server has VAC enabled

    version: StrType
    Version of the server software

    edf: int
    Extra data field, used to indicate if extra values are included in the response

    ping: float
    Round-trip time for the request in seconds, not actually sent by the server

    # Optional:
    port: Optional[int] = None
    Port of the game server.

    steam_id: Optional[int] = None
    Steam ID of the server

    stv_port: Optional[int] = None
    Port of the SourceTV server

    stv_name: Optional[StrType] = None
    Name of the SourceTV server

    keywords: Optional[StrType] = None
    Tags that describe the gamemode being played

    game_id: Optional[int] = None
    Game ID for games that have an app ID too high for 16bit.

    @property
    def has_port(self):
        return bool(self.edf & 0x80)

    @property
    def has_steam_id(self):
        return bool(self.edf & 0x10)

    @property
    def has_stv(self):
        return bool(self.edf & 0x40)

    @property
    def has_keywords(self):
        return bool(self.edf & 0x20)

    @property
    def has_game_id(self):
        return bool(self.edf & 0x01)
"""