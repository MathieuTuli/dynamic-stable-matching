"""Defines the agent class."""

class Agent():
    def __init__(self):
        self.id = None
        self.utilities = None
        self.match = None


class Man(Agent):
    id_counter = 0
    def __init__(self):
        super(Man).__init__(self)
        self.id = id_counter
        id_counter += 1


class Woman(Agent):
    id_counter = 0
    def __init__(self):
        super(Woman).__init__(self)
        self.id = id_counter
        id_counter += 1