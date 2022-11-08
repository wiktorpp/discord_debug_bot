import discord
from TOKEN import TOKEN
import debug

#import ...

client = discord.Client()

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")

#@client.event
#async def ...

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #...

    if message.content.startswith(debug.alias):
        await debug.run_message(message, locals())

client.run(TOKEN)   

