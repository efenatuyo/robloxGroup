import aiohttp, asyncio
from typing import Type
from ..cookie import RobloxCookie
from ..helpers import DotDict

class watch:
    messages: list = []
    checked_once = False
    def __init__(self, cookie: Type[RobloxCookie], group_id: int, prefix: str, group: Type[object]) -> None:
        self.cookie, self.group_id, self.prefix, self.group = cookie, group_id, prefix, group
        
    async def start(self) -> None:
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(f"https://groups.roblox.com/v2/groups/{self.group_id}/wall/posts?sortOrder=Desc&limit=100", cookies={".ROBLOSECURITY": self.cookie.cookie}, headers={"x-csrf-token": await self.cookie.x_token(session)}) as response:
                    if response.status == 200:
                        for message in (await response.json())["data"]:
                            if not message["id"] in self.messages:
                                self.messages.append(message["id"])
                                if self.checked_once:
                                    tasks = [self.group.handle_event("on_message", DotDict(message))]
                                    if message["body"].startswith(self.prefix):
                                        tasks.append(self.group.handle_command(message["body"].split(" ")[0][1:], DotDict(message), **{key: key for key in message["body"].split(" ")[1:]}))
                                    await asyncio.gather(*tasks)
                    elif response.status == 403:
                        rsp = await response.json()
                        if rsp["code"] != 0:
                            raise Exception(await response.json())
                    elif response.status == 400:
                        raise Exception(await response.json())
                    self.checked_once = True
                    await asyncio.sleep(3)