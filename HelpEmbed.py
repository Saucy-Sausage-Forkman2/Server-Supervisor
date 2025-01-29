import discord
def generate_help_embed():
    embed = discord.Embed(
        title="Help",
        color=discord.Colour.dark_gray()
    )
    embed.add_field(name=".create supervisor", value="Sends the results of a ping, and will update that message periodically. Dhar Mann will only update one supervisor per channel.")
    embed.add_field(name=".delete supervisor", value="Deletes the supervisor of the active channel, if there is one.")

    return embed
        