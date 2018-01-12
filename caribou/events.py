class Event():
    def __init__(self, agent):
        self.agent = agent


class EVevent(Event):
    def __init__(self, agent):
        super().__init__(agent)

    def set_next_event(self, energy_in=0, energy_out=0):
        if status


class PVevent(Event):
    def __init__(self, agent):
        super().__init__(agent)
        pass
