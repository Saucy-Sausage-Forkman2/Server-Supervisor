import discord
from JsonInterpreter import json_write, json_open, json_create_supervisor, json_remove_supervisor
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_ID=os.getenv("ADMIN_ID")

def generate_help_embed():
    embed = discord.Embed(
        title="Help",
        color=discord.Colour.dark_gray()
    )

    embed.add_field(name=".create supervisor", value="Sends the results of a ping, and will update that message periodically. Dhar Mann will only update one supervisor per channel.")
    embed.add_field(name=".delete supervisor", value="Deletes the supervisor of the active channel, if there is one.")

    return embed
        

async def convertMessageToCommand(message, prefix=""):
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