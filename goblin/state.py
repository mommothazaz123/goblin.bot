from .actor import Actor


class GoblinState:
    def __init__(self, init_model=True):
        self.red = None
        self.blue = None
        self.arena = None
        self.model = GoblinState(init_model=False) if init_model else None
        self.dist = 0

        # we probably aren't going to keep track of messages/bets in this client, but these are here for posterity
        self.log = []
        self.chat = []
        self.name = 'x'
        self.abilities = []
        self.score = 100
        self.bet_status = {}  # ?
        self.bet_returns = {}
        self.bet_totals = {}
        self.your_bet = {}
        self.confirmed = False
        self.last_bet = False
        self.dead = False
        self.returner = False
        self.muted = False
        self.last_chat = ''
        self.account = ''

    def connect(self, data):
        info = data['Info']
        self.arena = info['Arena']
        self.red = Actor(**info['Red'])
        self.blue = Actor(**info['Blue'])
        self.dist = info['Dist']

    def sync(self, data):
        self.model = GoblinState(init_model=False)
        self.model.connect(data)

    def set(self, data):
        prop = data.get('Info', {}).get('Prop') or data['Who']
        if prop == 'Red':
            self.red = self.model.red
        elif prop == 'Blue':
            self.blue = self.model.blue
        # todo other properties that we might care about
