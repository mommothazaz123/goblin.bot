import logging
import re
import time

import ete3
import ete3.treeview
from discord.ext import commands

from goblin.bracket import Bracket
from utils import img

log = logging.getLogger(__name__)


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bracket = Bracket()

        bot.goblin.register_listener('round_complete', self.round_complete)
        bot.goblin.register_listener('system_text', self.system_text)

    # ===== goblin event listeners =====
    async def round_complete(self, result):
        log.info(f"Round complete ({result.red.name} v. {result.blue.name}): victor is {result.victor.name}")
        result = self.bracket.merge(result.red, result.blue, result.victor)
        log.debug(result)
        await self.bot.goblin.download_image(result.red.image_path)
        await self.bot.goblin.download_image(result.blue.image_path)

    async def system_text(self, text):
        # bracket complete
        if re.search(r"wins the CR \d([\-/\s]+\d)? segment of the tournament", text):
            await self.bracket_complete(text)

        # tournament complete
        if re.search(r"is the grand ultimate tournament champion", text):
            await self.tournament_complete(text)

    async def bracket_complete(self, text):
        log.info(text)
        if len(self.bracket.matchups) != 1:
            log.warning(f"Bracket complete but more than 1 remaining matchup found! ({len(self.bracket.matchups)})")
            log.debug(self.bracket.matchups)
        await self.generate_tree()
        self.bracket.reset()

    async def tournament_complete(self, text):
        log.info(text)
        if len(self.bracket.matchups) != 1:
            log.warning(f"Tournament complete but more than 1 remaining matchup found! ({len(self.bracket.matchups)})")
            log.debug(self.bracket.matchups)
        self.bracket.reset()

    # ===== image generation =====
    async def generate_tree(self):
        t = ete3.Tree()

        async def recurse(node, matchup, wins_parent=True):
            if matchup.victor:
                fp = await self.bot.goblin.download_image(matchup.victor.image_path)
                p = img.crop_to_face(fp, matchup.victor)
                i = ete3.treeview.ImgFace(p)
                i.inner_background.color = '#677e52'
                i.inner_border.color = '#aaa98c'
                i.inner_border.width = 1
                if not wins_parent:
                    i.inner_background.color = '#695544'
                    i.opacity = 0.75
                node.add_face(i, 0)
                node.add_face(ete3.treeview.TextFace(matchup.victor.name), 0, position="branch-bottom")

            left = matchup.red
            if left:
                l_node = node.add_child()
                await recurse(l_node, left, (not matchup.victor) or matchup.victor.name == left.victor.name)

            right = matchup.blue
            if right:
                r_node = node.add_child()
                await recurse(r_node, right, (not matchup.victor) or matchup.victor.name == right.victor.name)

        await recurse(t, self.bracket.root())
        ts = ete3.treeview.TreeStyle()
        ts.optimal_scale_level = 'full'
        ts.show_leaf_name = False
        ts.force_topology = True
        ts.show_scale = False
        ts.branch_vertical_margin = 10
        t.render(f'logs/bracket-final-{int(time.time())}.png', tree_style=ts)


def setup(bot):
    bot.add_cog(Tracker(bot))
