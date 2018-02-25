""" Controllers of the simulation """

class GlobalController:
    def __init__(self, timer, localcontroller_list):
        self.timer = timer
        self.localcontroller_list

    def run_control(self):
        for localcontroller in localcontroller_list:
            localcontroller.run_control


class LocalController:
    def __init__(self, timer, agent_group, eventhandler):
        self.timer = timer
        self.agent_group = agent_group
        self.updated = False
        self.eventhandler = eventhandler
        self.end_simulation = 0

    def run_control(self):
        while self.end_simulation < len(agent_group):
            # control

            for agent in agent_group:
                if type(agent) is EV:
                    agent.charge_rate = 0
                    agent.gone = 0

    def check_time_max(self):
        return self.timer.time < self.timer.end_time

    def agent_end_simulation(self):
        self.end_simulation += 1



