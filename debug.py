import io
import sys
import traceback
import discord

async def run_message(message, other_locals):
    try:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        request_str = message.content[1:]
        
        try:
            exec(
                "async def request_funct(other_locals):\n"
                "    locals().update(other_locals)\n"
                f"    return_value = ({request_str})\n"
                "    globals().update(locals())\n"
                "    return return_value\n"
                "globals().update(locals())\n"
            )
        except:
            request = request.replace('\n', '\n    ')
            exec(
                "async def request_funct(other_locals):\n"
                "    locals().update(other_locals)\n"
                f"    {request_str}\n"
                "    globals().update(locals())\n"
                "globals().update(locals())\n"
            )
        return_value = await request_funct(locals())

        output = new_stdout.getvalue()
        sys.stdout = old_stdout

        if return_value != None:
            output = str(return_value) + "\n" + output
    except Exception:
        error = traceback.format_exc()
        await message.channel.send(f"```\n{error}\n```")
    else:
        if not len(output) > 2000:
            await message.channel.send(output)
        else:
            await message.channel.send(
                file=discord.File(io.BytesIO(output.encode()), 
                filename="output.txt")
            )