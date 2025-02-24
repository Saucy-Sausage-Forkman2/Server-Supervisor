import json

jsonFileName="StatusMessages.json"

def json_open():
    """Opens the json file that points to supervisor messages

    Returns:
        File: Json file: [Category][Channel ID] = Message ID
    """
    
    return open(f"{jsonFileName}","r")

def json_write(data):
    """Overwrites the json file. Returns nothing.

    Args:
        data (json): Output of json.dumps
    """

    with open(f"{jsonFileName}","r+") as json_file:
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file, indent=4)
        json_file.close()

    return

async def json_create_supervisor(channel, category):
    """Creates a supervisor of the specified category.

    Args:
        message (discord.message): The discord message object to gather necessary information from.
        category (str): The category to create the supervisor for.
    """

    category = f"{category}"
    pendingMessage = await channel.send("Pinging...")

    try:
        await json_remove_supervisor(channel.id,category,shouldPrint=False)

    except Exception as e: print(e)
        
    json_file = json_open()
    data = json.load(json_file)

    data[category].append({pendingMessage.channel.id:pendingMessage.id})
    json_write(data)

    await supervisor_loop(quickUpdate=True)

async def json_remove_supervisor(client, channelID, category,shouldPrint=True):
    """Removes the supervisor of the specified category.

    Args:
        message (discord.message): The discord message to find the channel from.
        category (str): _description_
    """

    category = f"{category}"

    json_file = json_open()
    data = json.load(json_file)
	
    dontcrash = await client.fetch_channel(channelID)
	
    for i in range(len(data[category])):
        
        try:

            try:
                dontcrash = await dontcrash.fetch_message(data[category][i][f"{channelID}"])

                await dontcrash.delete()
                if shouldPrint: await dontcrash.send("Supervisor disabled.")

            except Exception as e: 
                print(e)

            del data[category][i]

        except Exception as e: 
            print(e)
            continue

        else:
            json_write(data)

            return

    if shouldPrint: await dontcrash.send("There is no active supervisor in this channel.")

    return



