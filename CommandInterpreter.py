import discord
from JsonInterpreter import json_write, json_open, json_create_supervisor, json_remove_supervisor
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_ID=os.getenv("ADMIN_ID")

def generateHelpEmbed():
    """Returns an embed that shows how to use commands.

    Returns:
        (discord.Embed): Help Embed that explains commands.
    """

    embed = discord.Embed(
        title="Help",
        color=discord.Colour.dark_gray()
    )

    embed.add_field(name=".create supervisor <category>", value="Creates a supervisor in this channel with the servers of the specified category. There can only be one supervisor per category in the same channel.")
    embed.add_field(name=".delete supervisor <category>", value="Removes the supervisor of the specified category in this channel.")
    embed.add_field(name=".help", value="Show this help embed.")

    return embed

async def convertMessageToCommand(message, client, prefix=""):
    """Interprets a discord message into a command for the bot.

    Args:
        message (discord.Message): The message to process.
        prefix (str, optional): The prefix that the provided message must start with, otherwise it will be ignored. Defaults to no prefix.
    """
    
    if not message.content.startswith(prefix) or not message.author.id != ADMIN_ID:
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
                    await json_create_supervisor(message.channel, arguments[1])

                case _:
                    await message.channel.send(embed=generateHelpEmbed())

        case "delete":
            if len(arguments) < 2:
                await message.channel.send("Please provide a category.")
                return  

            match(arguments[0]):
                case "supervisor":
                    await json_remove_supervisor(client, message.channel.id, arguments[1])

                case _:
                    await message.channel.send(embed=generateHelpEmbed())
