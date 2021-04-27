import discord
from TOKEN import TOKEN
from asyncio import *
import io
import sys
from datetime import *

client = discord.Client()
setClient(client)

@client.event
async def on_ready():
    print("\033[31mLogged in as {0.user}\033[39m".format(client))

@client.event
async def on_message(message):
    globals().update(locals())

    #on_message.msg = message
    #on_message.message = message
    #old_stderr = sys.stderr
    #new_stderr = io.StringIO()
    #sys.stderr = new_stderr

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
            error = str(sys.exc_info())
            await message.channel.send(error)
        else:
            await pager(output, message.channel.send)

    globals().update(locals())

    #await message.channel.send(new_stderr.getvalue())
    #sys.stderr = old_stderr

client.run(TOKEN)

