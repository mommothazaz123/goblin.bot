import logging
import sys

import config
from bot import GoblinBot

bot = GoblinBot(command_prefix='!')

log_formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
log = logging.getLogger('bot')


@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name} ({bot.user.id})')


if __name__ == '__main__':
    bot.load_extension("cogs.tracker")
    bot.run(config.TOKEN)
