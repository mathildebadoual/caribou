""" Controllers of the simulation """

class GlobalController:
    def __init__(self, timer, localcontroller_list):
        self.timer = timer
        self.localcontroller_list

    def run_control(self):
        for localcontroller in localcontroller_list:
            localcontroller.run_control


class LocalController:
    def __init__(self, timer, agentgroup, eventhandler):
        self.timer = timer
        self.agentgroup = agentgroup
        self.updated = True
        self.eventhandler = eventhandler
        self.end_simulation = 0

    def run_control(self):
        pass

    def check_time_max(self):
        return self.timer.time < self.timer.end_time

    def agent_end_simulation(self):
        self.end_simulation += 1
