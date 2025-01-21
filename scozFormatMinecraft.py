import discord
from getTimestamp import time
def scozFormatMinecraft(java, bedrock, category, scozJavaAddress, scozBedrockAddress):
    zeroServerColor = discord.Colour.red()
    oneServerColor = discord.Colour.yellow()
    twoServerColor = discord.Colour.green()

    bothOnlineTitle = "Diesel Nation"
    onlyJavaTitle = "Diesel Nation: Bedrock Unreachable"
    onlyBedrockTitle = "Diesel Nation: Java Unreachable"
    bothOfflineTitle = "Diesel Nation is Offline"

    embed = 0
    
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
    
    embed.set_footer(text=time())

    #if java is online
    if java != 0:
        #if the server is alive
        version = java.version.name
        players = java.players.online
        maxPlayers=java.players.max
        javaPlayerList = java.players.sample
        #only java servers provide a list of active players

        embed.add_field(name="Players", value=f"{players}" + "/" + f"{maxPlayers}")
        if javaPlayerList != None:
            #go through the array of usernames and compile them into a list for beauty
            formattedUsernames = ""
            for i in javaPlayerList:
                formattedUsernames += " " + i.name + "\n"
            embed.add_field(name="", value=formattedUsernames,inline=True)
        else: embed.add_field(name="",value="",inline=True) # a new line to separate the player fields so it looks nice
        
        embed.add_field(name="", value="",inline=False)

        #I placed the player count before the Java server header as it applies to both java and bedrock, and it feels wrong to have the
        #player count only under one or under both. And it has to be exist.
        embed.add_field(name="Java", value="",inline=True)
        #Putting the game version first as it's the most important for new players, and is important in general
        embed.add_field(name="", value=f"{version}")

        #The java server has more details since both servers run hand in hand, so having all information about both is simply redundant.
        embed.add_field(name="",value=scozJavaAddress,inline=False)
    else:
        embed.add_field(name="",value="Server Offline")
    
    embed.add_field(name="",value="",inline=False) # a new line to separate the player fields so it looks nice

    #if bedrock is online
    if bedrock != 0:
        embed.add_field(name="Bedrock", value="")
        version = bedrock.version.name
        embed.add_field(name="  ", value=f"{version}")
        embed.add_field(name="",value=scozBedrockAddress,inline=False)
    else:
        embed.add_field(name="Bedrock",value="Server Offline")
    return embed