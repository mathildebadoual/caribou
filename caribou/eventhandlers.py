class EventHandler:
    def __init__(self, agent):
        self.agent = agent


class EVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)

class PVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)

# class HVACPowerConsumptionEventHandler(EventHandler):
#     def __init__(self):
#         EventHandler.__init__(self)


