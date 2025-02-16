import discord
import asyncio
import os
from dotenv import load_dotenv

from CommandInterpreter import convertMessageToCommand
from SupervisorLoop import supervisor_loop

prefix = '.'
updateDelayInSeconds = 60

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    await supervisor_loop(client, updateDelayInSeconds=updateDelayInSeconds)

@client.event
async def on_message(message):
    await convertMessageToCommand(message, client, prefix=prefix)

client.run(os.getenv('TOKEN'))







