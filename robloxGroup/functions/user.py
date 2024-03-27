import aiohttp, asyncio
from ..helpers import DotDict
from typing import Type, Union

async def followers(group: Type[object], user_id: Union[str, int], get_all: bool = False):
    responses = {}
    cursor = ""
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followers?cursor={cursor}&sortOrder=Desc&limit=100", cookies={".ROBLOSECURITY": group.cookie.cookie}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
                if response.status == 200:
                    response = await response.json()
                    if responses:
                        response["data"] += responses["data"]
                        responses = response
                    else:
                        responses = response
                    if not get_all or not response.get("nextPageCursor"):
                        return DotDict(responses)
                    else:
                        cursor = response["nextPageCursor"]
                elif response.status == 429:
                    print("ratelimit exceeded. Sleeping 20 seconds")
                    await asyncio.sleep(20)
