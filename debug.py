import discord
from TOKEN import TOKEN
from asyncio import *
import io
import sys
from datetime import *
from pager import pager
import traceback

client = discord.Client()

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))

@client.event
async def on_message(message):
    
    #...
    
    if message.content.startswith("$report"):
        await message.channel.send("Status: online")

    if message.content.startswith("%"):
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            progArr = message.content[1:].splitlines()
            progStrIndented = ""
            for i in progArr:
                progStrIndented += "\n    " + i
            exec(
                "async def t():" +
                progStrIndented +
                "\n    globals().update(locals())",
                globals()
            )
            await t()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            await pager(output, message.channel.send)

    globals().update(locals())

client.run(TOKEN)

