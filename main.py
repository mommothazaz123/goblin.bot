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


@bot.goblin.listener()
async def temp(data):
    if (not data.get('Text')) or data.get('Type') == 'Chat':
        return
    text = data['Text']
    await bot.get_channel(810638145636139049).send(text)

@bot.goblin.listener('round_complete')
async def round_complete(result):
    log.info(f"Round complete ({result.red.name} v. {result.blue.name}): victor is {result.victor.name}")

if __name__ == '__main__':
    bot.run(config.TOKEN)
