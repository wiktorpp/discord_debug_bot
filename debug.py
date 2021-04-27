from libDiscordTools import *
import sys
from traceback import *

async def debug(message):
    if message.content.startswith("%"):
        try:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            progArr = message.content[1:].splitlines()
            progStrInd = ""
            for i in progArr:
                progStrInd += "\n    " + i
            exec(
                "async def t():"
                + progStrInd
                + "\n    globals().update(locals())",
                globals()
            )
            await t()

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

        except:
            error = sys.exc_info()
            debug.error = error
            await message.channel.send(error)
        else:
            await pager(output, message.channel.send)
