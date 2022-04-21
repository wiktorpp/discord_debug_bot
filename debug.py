import discord
from TOKEN import TOKEN

import io
import sys
import traceback
import textwrap

#import ...

client = discord.Client()

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")

@client.event
async def on_message(message):
    
    #...

    if message.content.startswith("%"):
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            request = message.content[1:]
            exec(
                "async def request_funct():\n" +
                "    " + request.replace("\n", "\n    ") + "\n"
                "    globals().update(locals())",
                globals()
            )
            await request_funct()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            import textwrap
            for chunk in textwrap.wrap(output, 2000, replace_whitespace=False):
                await message.channel.send(chunk)

client.run(TOKEN)

