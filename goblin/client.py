import asyncio
import collections
import logging
import traceback
import typing

import aiohttp

from .events import RoundComplete, StartRound
from .state import GoblinState

log = logging.getLogger(__name__)


# log.setLevel(logging.DEBUG)


class GoblinClient:
    def __init__(self, http_base="http://goblin.bet:5000", ws_base="ws://goblin.bet:5000"):
        self.http_base: str = http_base
        self.ws_base: str = ws_base

        self.state: GoblinState = GoblinState()  # initialize to an empty state, we'll populate this later
        self.ws: typing.Optional[aiohttp.ClientWebSocketResponse] = None
        self.http: typing.Optional[aiohttp.ClientSession] = None
        self.task: typing.Optional[asyncio.Task] = None

        self.listeners = collections.defaultdict(lambda: [])  # {event_type: [listeners]}
        self._handlers = {
            'Connect': self.handle_connect,
            'Sync': self.handle_sync,
            'Set': self.handle_set,
            'NewBattle': self.handle_new_battle,
            'StartRound': self.handle_start_round,
            'RoundComplete': self.handle_round_complete,
        }

    # lifecycle methods: connect -> start -> close
    async def connect(self):
        self.http = aiohttp.ClientSession()
        self.ws = await self.http.ws_connect(self.ws_base)

    async def start(self):
        self.task = asyncio.create_task(self.do_ws())

    async def do_ws(self):
        connect = await self.ws.receive_json()  # CONNECT packet
        await self.handle_event(connect)

        log.info(await self.ws.receive_str())  # random debug packet?

        # main game loop
        while True:
            try:
                msg = await self.ws.receive_json()
                await self.handle_event(msg)
            except Exception:
                traceback.print_exc()

    async def close(self):
        if self.task is not None:
            self.task.cancel()
        await self.ws.close()
        await self.http.close()

    # ws handler
    async def handle_event(self, data: dict):
        log.debug(f"RECV: {data}")
        if 'Type' not in data:
            data['Type'] = ''  # log message, text field

        await self.dispatch('event_raw_receive', data)
        handler = self._handlers.get(data['Type'])
        if handler:
            # noinspection PyArgumentList
            await handler(data)
        elif data['Type']:
            log.info(f"No handler for event type {data['Type']!r}")

    async def handle_connect(self, data):
        log.debug("CONN")
        self.state.connect(data)

    async def handle_sync(self, data):
        log.debug("SYNC")
        self.state.sync(data)

    async def handle_set(self, data):
        log.debug("SET ")
        self.state.set(data)

    async def handle_new_battle(self, data):
        pass

    async def handle_start_round(self, data):
        log.debug("STRT")
        await self.dispatch('start_round', StartRound(self.state, **data))

    async def handle_round_complete(self, data):
        log.debug("END ")
        await self.dispatch('round_complete', RoundComplete(self.state, **data))

    # listeners
    async def dispatch(self, event_type: str, *args, **kwargs):
        for listener in self.listeners[event_type]:
            try:
                await listener(*args, **kwargs)
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
