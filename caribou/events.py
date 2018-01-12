
class Event():
    def __init__(self, agent):
        self.agent = agent

    def run_next_step(self):
        self.run_step()
        self.current_time_step += 1

    def run_step(self):
        raise NotImplementedError


class EVevent(Event):
    def __init__(self, agent):
        super().__init__(agent)


class EVCharging(EVevent): # can inherit from Event
    def __init__(self, agent):
        super().__init__(agent)


class PVevent(Event):
    def __init__(self, agent):
        super().__init__(agent)
