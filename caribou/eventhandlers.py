
class EventHandlers():
    def __init__(self):
        self.list_events = []
        self.startegy = []

    def set_list_events(self, list_events):
        self.list_events = list_events

    def get_list_events(self):
        return self.list_events

    def set_strategy(self, strategy):
        self.startegy = strategy

    def add_strategy(self, event):
        self.strategy.append(event)

    def get_strategy(self):
        return self.strategy

    def start_simulation(self):
        pass

    def pass_event(self):
        pass
