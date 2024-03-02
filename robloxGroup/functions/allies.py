import aiohttp
from typing import Type, Union
from ..helpers import DotDict
from ..commands import Bot

async def get(group: Type[Bot]) -> Type[DotDict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://groups.roblox.com/v1/groups/{group.group_id}/relationships/allies?maxRows=100&sortOrder=Asc&startRowIndex=0", cookies={".ROBLOSECURITY": group.cookie.cookie}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
                return DotDict(await response.json())