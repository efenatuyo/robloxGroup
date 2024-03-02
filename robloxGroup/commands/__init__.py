from ..listeners import group_wall
from ..cookie    import Bypass, RobloxCookie
from   typing    import Awaitable, Callable
from typing import Union
import asyncio, inspect

class Bot:
    commands: dict = {}
    events: dict = {}
    def __init__(self, prefix: str, group_id: Union[int, str], cookie: str) -> None:
        self.cookie = RobloxCookie(Bypass(cookie).get_set_cookie())
        self.prefix = prefix
        self.group_id = group_id

    def command(self, func: Callable[..., Awaitable[None]]) -> str:
        event_name = func.__name__
        if event_name in self.commands:
            raise ValueError(f"Command '{event_name}' already exists.")
        self.commands[event_name] = func
        return func
    
    def event(self, func: Callable[..., Awaitable[None]]) -> str:
        event_name = func.__name__
        if event_name in self.events:
            raise ValueError(f"Event '{event_name}' already exists.")
        self.events[event_name] = func
        return func

    async def handle_command(self, event_name: str, ctx, **args) -> Awaitable[None]:
        if event_name in self.commands:
            command_func = self.commands[event_name]
            command_args = inspect.signature(command_func).parameters
            if len(args) != len(command_args) - 1:
                expected_args = ", ".join(command_args)
                received_args = ", ".join(map(str, args))
                print(f"Number of arguments for '{event_name}' does not match. Expected: {expected_args}, but got: {received_args}")
            return await self.commands[event_name](ctx, *args)
        
    async def handle_event(self, event_name: str, ctx, **args) -> Awaitable[None]:
        if event_name in self.events:
            command_func = self.events[event_name]
            command_args = inspect.signature(command_func).parameters
            if len(args) != len(command_args) - 1:
                expected_args = ", ".join(command_args)
                received_args = ", ".join(map(str, args))
                print(f"Number of arguments for '{event_name}' does not match. Expected: {expected_args}, but got: {received_args}")
            return await self.events[event_name](ctx, *args)
            
    async def run(self) -> None:
        tasks = [group_wall.watch(cookie=self.cookie, group_id=self.group_id, group=self, prefix=self.prefix).start()]
        await asyncio.gather(*tasks)