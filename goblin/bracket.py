from .actor import Actor, BaseActor


class Bracket:
    """A forest of matchup trees. After each match, two trees are merged."""

    def __init__(self):
        self.matchups = []  # type: list[Matchup]

    def merge(self, red: Actor, blue: Actor, victor: BaseActor):
        """After a round completes, merge (or create) two Matchups representing the round and outcome."""
        # todo don't merge prior bracket's winner's tstats?
        red_tree = self.pop_tree(red, create=True)
        blue_tree = self.pop_tree(blue, create=True)
        new_tree = Matchup(red_tree, blue_tree, victor)
        self.matchups.append(new_tree)
        return new_tree

    def pop_tree(self, root_actor: Actor, create: bool = False):
        """
        Returns the tree that has the specified actor as its root, or creates one if said tree is not found and
        ``create`` is True.

        :rtype: Matchup
        """
        existing = next((m for m in self.matchups if m.victor.name == root_actor.name), None)
        if existing:
            self.matchups.remove(existing)
            return existing
        if not create:
            raise ValueError("Root matchup not found")
        return Matchup.from_actor(root_actor)

    def root(self):
        """Creates a Matchup representing a possible full bracket."""
        matchups = self.matchups.copy()
        while len(matchups) > 1:
            left = matchups.pop()
            right = matchups.pop()
            matchups.insert(0, FutureMatchup(red=left, blue=right, victor=None))
        return matchups[0]


class Matchup:
    def __init__(self, red, blue, victor):
        """
        :type red: Matchup or None
        :type blue: Matchup or None
        :type victor: BaseActor
        """
        self.red = red
        self.blue = blue
        self.victor = victor

    @classmethod
    def from_actor(cls, actor: Actor):
        """Generate a Matchup tree given an actor and its ``tstats``."""

        def recurse(tstats):
            if not tstats:
                return cls(red=None, blue=None, victor=actor)
            defeated = Matchup(red=None, blue=None, victor=BaseActor(name=tstats[-1]))
            return cls(red=recurse(tstats[:-1]), blue=defeated, victor=actor)

        return recurse(actor.t_stats)

    def __repr__(self):
        return f"<{self.__class__.__name__} red={self.red!r} blue={self.blue!r} victor={self.victor!r}>"


class FutureMatchup(Matchup):
    def __init__(self, red, blue, victor):
        """
        :type victor: BaseActor or None
        """
        super().__init__(red, blue, victor)
