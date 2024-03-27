import aiohttp, asyncio
from typing import Type, Union
from ..helpers import DotDict
from ..commands import Bot

async def get(group: Type[Bot], get_all: bool = False) -> Type[DotDict]:
    responses = {}
    current = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"https://groups.roblox.com/v1/groups/{group.group_id}/relationships/allies?maxRows=100&sortOrder=Asc&startRowIndex={current}", cookies={".ROBLOSECURITY": group.cookie.cookie}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
                if response.status == 200:
                    response = await response.json()
                    current += 100
                    if responses:
                        response["relatedGroups"].append(responses["relatedGroups"])
                        responses = responses 
                    else:
                        responses = response
                    responses.update(response)
                    if not get_all or responses.get("nextRowIndex") == 0:
                        return DotDict(responses)
                    else:
                        current = responses.get("nextRowIndex")
                elif response.status == 429:
                    print("ratelimit exceeded. Sleeping 20 seconds")
                    await asyncio.sleep(20)
                elif response.status == 400:
                    return DotDict(responses)