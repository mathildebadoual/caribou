import numpy as np
import caribou.events as events
import caribou.agents as agents

HOURS_PER_DAY = 24

class EventHandlers():
    def __init__(self, agentgroup, data_generator, plot_callback=None):
        self.startegy = {}
        self.agentgroup = agentgroup
        self.data_generator = data_generator
        self.plot_callback = plot_callback
        self.ev_events = []
        self.pv_events = []

    def create_events(self):
        for agent in self.agentgroup.get_list_agents():
            if isinstance(agent, agents.EV):
                self.ev_events.append(events.EVevents(agent))
            if isinstance(agent, agents.PV):
                self.pv_events.append(events.PVevents(agent))

    def get_strategy(self):
        return self.startegy

# TODO(Mathilde): Change this function to have multiples pvs or evs

    def create_startegy(self, control_values):
        load_from_grid = control_values[:HOURS_PER_DAY]
        ev_store = control_values[HOURS_PER_DAY:]
        for hour in range(HOURS_PER_DAY):
            for ev_event in ev_events:
                ev_event.
            self.strategy{0} = {'ev_event': ev_event


    def start_simulation(self):
        pass

    def pass_event(self):
        pass

    def plot_results(self):
        pass
