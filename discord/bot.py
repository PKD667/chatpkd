import discord,dotenv
from .. import Conversation, log

client = discord.Client()
cbot = Conversation()
cbot.load(filename="default.json")
# load the project files
cbot.add_files(["bot.py", "main.py"])

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif 'comrade' in message.content.lower() or client.user.mentioned_in(message):
        if message.author.name == "PKD":
            print("PKD is talking to me")
            cbot.append("system", f"{message.content}")
        else :
            cbot.append("user", f" {message.author.name} : {message.content}")
        response = cbot.get_response()
        cbot.append(response["role"], response["content"])
        
        # check if the response is longer than 2000 characters
        if len(response["content"]) <= 2000:
            await message.channel.send(response["content"])
        else:
            # split the response into chunks of 2000 characters
            chunks = [response["content"][i:i+2000] for i in range(0, len(response["content"]), 2000)]
            for chunk in chunks:
                await message.channel.send(chunk)
        
        log(f"{message.author.name} : {message.content.lower()}", filename="bot.log")

client.run(dotenv.get_key(".env", "DISCORD_TOKEN"))
