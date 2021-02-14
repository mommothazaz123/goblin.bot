import asyncio
import collections
import itertools
import logging
import typing

import aiohttp

from .state import GoblinState

log = logging.getLogger(__name__)


class GoblinClient:
    def __init__(self, http_base="http://goblin.bet:5000", ws_base="ws://goblin.bet:5000"):
        self.http_base: str = http_base
        self.ws_base: str = ws_base

        self.state: GoblinState = GoblinState()  # initialize to an empty state, we'll populate this later
        self.ws: typing.Optional[aiohttp.ClientWebSocketResponse] = None
        self.http: typing.Optional[aiohttp.ClientSession] = None
        self.task: typing.Optional[asyncio.Task] = None

        self.listeners = collections.defaultdict(lambda: [])  # {event_type: [listeners]}

    # lifecycle methods: connect -> start -> close
    async def connect(self):
        self.http = aiohttp.ClientSession()
        self.ws = await self.http.ws_connect(self.ws_base)

    async def start(self):
        self.task = asyncio.create_task(self.do_ws())

    async def do_ws(self):
        connect = await self.ws.receive_json()  # CONNECT packet
        await self.handle_connect(connect)

        await self.ws.receive_str()  # random debug packet?

        # main game loop
        while True:
            msg = await self.ws.receive_json()
            await self.handle_event(msg)

    async def close(self):
        if self.task is not None:
            self.task.cancel()
        await self.ws.close()
        await self.http.close()

    # ws handlers
    async def handle_connect(self, data: dict):
        log.debug(f"RECV: {data}")
        log.debug("Handling connect packet")
        self.state.connect(data)
        await self.dispatch(data['Type'], data)

    async def handle_event(self, data: dict):
        log.debug(f"RECV: {data}")
        await self.dispatch(data['Type'], data)

    # listeners
    async def dispatch(self, event_type: str, data: dict):
        for listener in itertools.chain(self.listeners[None], self.listeners[event_type]):
            try:
                await listener(data)
            except Exception as e:
                log.warning(f"Unhandled error in dispatch: {e}")

    def register_listener(self, event_type: typing.Optional[str], coro: typing.Coroutine):
        """
        Registers a listener that is called every time an ``event_type`` event is received. If ``event_type`` is None
        the listener will be called for all events (before the event-specific listeners).
        """
        log.debug(f"Registered listener for {event_type!r}")
        self.listeners[event_type].append(coro)

    # decorator way of registering listener
    def listener(self, event_type: typing.Optional[str] = None):
        def wrapper(func):
            self.register_listener(event_type, func)
            return func

        return wrapper
