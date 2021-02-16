class Event:
    def __init__(self, **data):
        self.type = data.get('Type', 'Unknown')
        self.text = data.get('Text')
        self.connections = data.get('Connections')


class StartRound(Event):
    def __init__(self, state, **data):
        super().__init__(**data)
        self.state = state
        self.red = state.red
        self.blue = state.blue


class RoundComplete(Event):
    def __init__(self, state, **data):
        super().__init__(**data)
        self.state = state
        self.red = state.red
        self.blue = state.blue
        self.victor = self.red if data['Who'] == 'Red' else self.blue
