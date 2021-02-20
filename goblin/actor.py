from dataclasses import dataclass


class BaseActor:
    def __init__(self, name):
        self.name = name

    @property
    def image_path(self):
        return f"/Art/{self.name.replace(' ', '')}.png"

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"


class Actor(BaseActor):
    def __init__(self, name: str, cr: int, max_hp: int, ac: int, stats, tags, size: int, movement, skills, saves,
                 senses, languages, actions, immune, resist, vulnerable, conditions, c_info, vis, events, e_info,
                 concentration, act_econ, face, target, id, t_stats=None, init=None):
        if t_stats is None:
            t_stats = []

        super().__init__(name)
        self.cr: int = cr
        self.max_hp = max_hp
        self.ac = ac
        self.stats = stats
        self.tags = tags
        self.size = size
        self.movement = movement
        self.skills = skills
        self.saves = saves
        self.senses = senses
        self.languages = languages
        self.actions = actions
        self.immune = immune
        self.resist = resist
        self.vulnerable = vulnerable
        self.conditions = conditions
        self.c_info = c_info
        self.vis = vis
        self.events = events
        self.e_info = e_info
        self.concentration = concentration
        self.act_econ = act_econ
        self.face = face
        self.t_stats = t_stats
        self.target = target
        self.id = id
        self.init = init

    @classmethod
    def from_data(cls, data):
        face = FaceLocation.from_data(data['Face'])
        return cls(
            name=data['Name'], cr=data['CR'], max_hp=data['MaxHP'], ac=data['AC'], stats=data['Stats'],
            tags=data['Tags'], size=data['Size'], movement=data['Movement'], skills=data['Skills'], saves=data['Saves'],
            senses=data['Senses'], languages=data['Languages'], actions=data['Actions'], immune=data['Immune'],
            resist=data['Resist'], vulnerable=data['Vulnerable'], conditions=data['Conditions'], c_info=data['CInfo'],
            vis=data['Vis'], events=data['Events'], e_info=data['EInfo'], concentration=data['Concentration'],
            act_econ=data['ActEcon'], face=face, t_stats=data.get('TStats', []), target=data['Target'], id=data['ID'],
            init=data.get('Init')
        )


@dataclass
class FaceLocation:
    x: int
    y: int

    @classmethod
    def from_data(cls, data):
        return cls(data['X'], data['Y'])
