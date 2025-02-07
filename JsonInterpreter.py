import json

jsonFileName="StatusMessages.json"

def json_open():
    return open(f"{jsonFileName}","r")

def json_write(data):
    with open(f"{jsonFileName}","r+") as json_file:
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file, indent=4)
        json_file.close()

    return

async def json_create_supervisor(message, category):
    category = f"{category}"
    pendingMessage = await message.channel.send("Pinging...")

    try:
        await json_remove_supervisor(message,category,shouldPrint=False)

    except Exception as e: print(e)
        
    json_file = open_json(jsonFileName)
    data = json.load(json_file)

    data[category].append({pendingMessage.channel.id:pendingMessage.id})
    write_json(data,jsonFileName)

    await supervisor_loop(quickUpdate=True)

async def json_remove_supervisor(message, category,shouldPrint=True):
    category = f"{category}"

    json_file = open_json(jsonFileName)
    data = json.load(json_file)

    for i in range(len(data[category])):
        try:

            try:
                dontcrash = await client.fetch_channel(message.channel.id)
                dontcrash = await dontcrash.fetch_message(data[category][i][f"{message.channel.id}"])

                await dontcrash.delete()

            except Exception as e: 
                print(e)

            del data[category][i]

        except Exception as e: 
            print(e)
            continue

        else:
            write_json(data,jsonFileName)
            if shouldPrint: await message.channel.send("Supervisor disabled.")

            return

    if shouldPrint: await message.channel.send("There is no active supervisor in this channel.")

    return



