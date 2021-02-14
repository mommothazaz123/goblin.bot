from discord.ext.commands import Bot

from goblin import GoblinClient


class GoblinBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.goblin = GoblinClient()

    async def start(self, *args, **kwargs):
        await self.goblin.connect()
        await self.goblin.start()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.goblin.close()
        await super().close()
