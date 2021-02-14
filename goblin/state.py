class GoblinState:
    def __init__(self):
        self.red = None
        self.blue = None
        self.arena = None
        self.model = None
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
        if data['Type'] != 'Connect':
            raise ValueError("Non-connect type packet passed to connect handler")
        info = data['Info']
        self.arena = info['Arena']
        self.red = info['Red']
        self.blue = info['Blue']
        self.dist = info['Dist']


{
    'Type': 'Connect',
    'Info': {
        'BetOdds': {'Red': 1.2, 'Blue': 1},
        'Arena': {'Name': 'Forest', 'Img': 'Forest', 'Weight': 5, 'Dist': 30, 'Blinded': {}, 'CantMove': {'Swim': 0}},
        'Red': {
            'Name': 'Copper Dragon Wyrmling',
            'CR': 1,
            'HP': 15,
            'MaxHP': 22,
            'AC': 16,
            'Stats': {'STR': 15, 'DEX': 12, 'CON': 13, 'INT': 14, 'WIS': 11, 'CHA': 13},
            'Tags': {'Dragon': {'Shown': True}, 'Chaotic': {'Shown': True}, 'Good': {'Shown': True}},
            'Size': 1,
            'Movement': {'Speed': 30, 'Climb': 30, 'Flying': 60},
            'Skills': {'Perception': 4, 'Stealth': 3},
            'Saves': {'WIS': 2, 'DEX': 3, 'CON': 3, 'CHA': 3},
            'Senses': {'Normal': 999, 'Dark': 60, 'Blind': 10},
            'Languages': {'Draconic': {}},
            'Actions': {
                'Bite': {
                    'Name': 'Bite',
                    'Acc': 3,
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 5,
                    'Tags': {'Weapon': {}, 'Attack': {}, 'Melee': {}},
                    'Priority': 5,
                    'Hit': [
                        {'Type': 'Damage', 'Amount': '1d10+2', 'DType': 'Piercing'}
                    ],
                    'Miss': [],
                    'Effect': [],
                    'PreEffect': [],
                    'Text': '%s attacks %t with a %a.',
                    'AI': {}
                },
                'Breath Weapon': {
                    'Name': 'Breath Weapon',
                    'Acc': None,
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 20,
                    'Tags': {'Breath Weapon': {}, 'Attack': {}, 'AoE': {}},
                    'Priority': 6,
                    'Hit': [],
                    'Miss': [],
                    'Effect': [{
                        'Type': 'Actions',
                        'Random': 1,
                        'Actions': {'Acid Breath': 1, 'Slowing Breath': 1}
                    }],
                    'PreEffect': [],
                    'Text': '',
                    'AI': {},
                    'MaxUses': 1,
                    'Uses': 0,
                    'Recharge': 5,
                    'IdealRange': 15
                },
                'Acid Breath': {
                    'Name': 'Acid Breath',
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 20,
                    'Tags': {'Breath Weapon': {}, 'Attack': {}, 'AoE': {}},
                    'Priority': -1,
                    'Hit': [],
                    'Miss': [],
                    'Effect': [{
                        'Type': 'SDamage',
                        'Amount': '4d8',
                        'Save': 'DEX',
                        'DC': 11,
                        'DType': 'Acid'
                    }],
                    'PreEffect': [],
                    'Text': '%s uses %a.',
                    'AI': {}
                },
                'Slowing Breath': {
                    'Name': 'Slowing Breath',
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 15,
                    'Tags': {'Breath Weapon': {}, 'Attack': {}, 'AoE': {}},
                    'Priority': -1,
                    'Hit': [],
                    'Miss': [],
                    'Effect': [{
                        'Type': 'Condition',
                        'Condition': 'Slowed',
                        'Save': 'CON',
                        'DC': 11,
                        'Duration': 1,
                        'EndDC': 11,
                        'EndStat': 'CON'
                    }],
                    'PreEffect': [],
                    'Text': '%s uses %a.',
                    'AI': {}
                }
            },
            'Immune': {'Acid': {'Show': True}},
            'Resist': {},
            'Vulnerable': {},
            'Conditions': {},
            'CInfo': {},
            'Vis': {},
            'Events': {},
            'EInfo': {},
            'Concentration': '',
            'ActEcon': {'Action': 0, 'Bonus': 1, 'Reaction': 1, 'Move': 60, 'MType': 'Flying'},
            'Face': {'X': 39, 'Y': 64},
            'TStats': ['Spy'],
            'Target': 'Blue',
            'ID': 'Red',
            'Init': 12
        },
        'Blue': {
            'Name': 'Animated Armor',
            'CR': 1,
            'HP': 1,
            'MaxHP': 33,
            'AC': 18,
            'Stats': {'STR': 14, 'DEX': 11, 'CON': 13, 'INT': 1, 'WIS': 3, 'CHA': 1},
            'Tags': {'Construct': {'Shown': True}, 'Unaligned': {'Shown': True}, 'Magic Powered': {},
                     'Metal Armor': {}},
            'Size': 1,
            'Movement': {'Speed': 25},
            'Skills': {},
            'Saves': {},
            'Senses': {'Blind': 60},
            'Languages': {},
            'Actions': {
                'Multiattack': {
                    'Name': 'Multiattack',
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 5,
                    'Tags': {'Melee': {}, 'Weapon': {}, 'Attack': {}, 'Multiattack': {}},
                    'Priority': 5,
                    'Hit': [],
                    'Miss': [],
                    'Effect': [{'Type': 'Actions', 'Actions': {'Slam': 2}}],
                    'PreEffect': [],
                    'Text': '',
                    'AI': {}
                },
                'Slam': {
                    'Name': 'Slam',
                    'Acc': 3,
                    'Target': {'Type': 'Enemy', 'Num': 1},
                    'Def': 'AC',
                    'Range': 5,
                    'Tags': {'Melee': {}, 'Weapon': {}, 'Attack': {}},
                    'Priority': 4,
                    'Hit': [{'Type': 'Damage', 'Amount': '1d6+2', 'DType': 'Bludgeoning'}],
                    'Miss': [],
                    'Effect': [],
                    'PreEffect': [],
                    'Text': '%s attacks %t with a %a.',
                    'AI': {}
                }
            },
            'Immune': {'Poison': {'Show': True}, 'Psychic': {'Show': True},
                       'Blinded': {'Show': True}, 'Charmed': {'Show': True},
                       'Deafened': {'Show': True}, 'Exhaustion': {'Show': True},
                       'Frightened': {'Show': True}, 'Paralyzed': {'Show': True},
                       'Petrified': {'Show': True}, 'Poisoned': {'Show': True}},
            'Resist': {},
            'Vulnerable': {},
            'Conditions': {},
            'CInfo': {},
            'Vis': {},
            'Events': {},
            'EInfo': {},
            'Concentration': '',
            'ActEcon': {'Action': 0, 'Bonus': 1, 'Reaction': 1, 'Move': 25, 'MType': 'Speed'},
            'Face': {'X': 44, 'Y': 70},
            'Condition': {'Hidden': {}},
            'TStats': ['Giant Vulture'],
            'Target': 'Red',
            'ID': 'Blue',
            'Init': 18
        },
        'Dist': 5,
        'BetsLocked': True
    }
}
