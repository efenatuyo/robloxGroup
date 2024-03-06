import aiohttp, asyncio
from typing import Type, Union
from ..cookie import RobloxCookie
from ..helpers import DotDict
from ..functions import role
class watch:
    users: list = []
    checked_once = False
    def __init__(self, cookie: Type[RobloxCookie], group: Type[object]) -> None:
        self.cookie, self.group = cookie, group
        
    async def start(self) -> None:
        on_join_role = (await role.get(self.group)).roles[1].id
        async with aiohttp.ClientSession() as session:
            while True:
              try:
                async with session.get(f"https://groups.roblox.com/v1/groups/{self.group.group_id}/roles/{on_join_role}/users?cursor=&limit=100&sortOrder=Desc", cookies={".ROBLOSECURITY": self.cookie.cookie}, headers={"x-csrf-token": await self.cookie.x_token(session)}) as response:
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
              except: 
                  pass
              finally: 
                  self.checked_once = True
                  await asyncio.sleep(3)
