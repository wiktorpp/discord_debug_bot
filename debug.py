import discord
from TOKEN import TOKEN

#import ...

client = discord.Client()

@client.event
async def on_ready():
    print(f"\033[31mLogged in as {client.user}\033[39m")

@client.event
async def on_message(message):
    
    #...

    if message.content.startswith("%"):
        import io
        import sys
        import traceback
        import textwrap
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            request = message.content[1:]
            try:
                exec(
                    "async def request_funct():\n" +
                    "    return_value = (" + request + ")" + "\n"
                    "    globals().update(locals())\n"
                    "    return return_value",
                    globals()
                )
            except:
                exec(
                    "async def request_funct():\n" +
                    "    " + request.replace("\n", "\n    ") + "\n"
                    "    globals().update(locals())\n"
                    "    return None",
                    globals()
                )
            return_value = await request_funct()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            if return_value != None:
                output = str(return_value) + "\n" + output
        except:
            error = traceback.format_exc()
            await message.channel.send(error)
        else:
            for chunk in textwrap.wrap(output, 2000, replace_whitespace=False):
                await message.channel.send(chunk)

client.run(TOKEN)

