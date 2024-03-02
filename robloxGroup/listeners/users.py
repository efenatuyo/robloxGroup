import aiohttp, asyncio
from typing import Type
from ..cookie import RobloxCookie
from ..helpers import DotDict

class watch:
    users: list = []
    checked_once = False
    def __init__(self, cookie: Type[RobloxCookie], group_id: int, group: Type[object]) -> None:
        self.cookie, self.group_id, self.group = cookie, group_id, group
        
    async def start(self) -> None:
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(f"https://groups.roblox.com/v1/groups/{self.group_id}/roles/80273647/users?cursor=&limit=100&sortOrder=Desc", cookies={".ROBLOSECURITY": self.cookie.cookie}, headers={"x-csrf-token": await self.cookie.x_token(session)}) as response:
                    if response.status == 200:
                        for user in (await response.json())["data"]:
                            if not user["userId"] in self.users:
                                self.users.append(user["userId"])
                                if self.checked_once:
                                    await self.group.handle_event("on_member_join", DotDict(user))
                    elif response.status == 403:
                        rsp = await response.json()
                        if rsp["code"] != 0:
                            raise Exception(await response.json())
                    elif response.status == 400:
                        raise Exception(await response.json())
                    self.checked_once = True
                    await asyncio.sleep(3)