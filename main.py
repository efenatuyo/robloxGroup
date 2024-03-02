import asyncio
from robloxGroup import commands
from robloxGroup.functions import role, allies
group = commands.Bot(prefix="!", group_id=0, cookie="_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|")

@group.command
async def command_name(ctx, args):
    pass

@group.event
async def on_message(ctx):
    pass

asyncio.run(group.run())
