import aiohttp
from typing import Type, Union
from ..helpers import DotDict

async def change(group: Type[object], user_id: Union[int, str], role_id: Union[int, str]) -> Type[DotDict]:
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"https://groups.roblox.com/v1/groups/{group.group_id}/users/{user_id}", cookies={".ROBLOSECURITY": group.cookie.cookie}, json={"roleId": role_id}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
            return DotDict(await response.json())

async def guilds_user(group: Type[object], user_id: Union[int, str]) -> Type[DotDict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles?includeLocked=false", cookies={".ROBLOSECURITY": group.cookie.cookie}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
            return DotDict(await response.json())

async def get(group: Type[object]) -> Type[DotDict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://groups.roblox.com/v1/groups/{group.group_id}/roles", cookies={".ROBLOSECURITY": group.cookie.cookie}, headers={"x-csrf-token": await group.cookie.x_token(session)}) as response:
            return DotDict(await response.json())
