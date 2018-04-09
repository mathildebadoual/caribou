import caribou.solvers as solvers
import cvxpy
import numpy as np

""" Controllers of the simulation """


class GlobalController:
    def __init__(self, timer, localcontroller_list):
        self.timer = timer
        self.localcontroller_list

    def run_control(self):
        for localcontroller in localcontroller_list:
            localcontroller.run_control



def GlobalControllerModel1(GlobalController):
    def __init__(self):
        super().__init__()



class LocalController:
    def __init__(self, timer, agentgroup, eventhandler):
        self.timer = timer
        self.agentgroup = agentgroup
        self.updated = True
        self.eventhandler = eventhandler
        self.end_simulation = 0
        self.state_vector = [0, 0, 0, 0]  # [\dot{soc_ev}, soc_ev, \dot{soc_b}, soc_b]

    def run_control(self):
        while self.end_simulation < len(self.agentgroup.agents_list):
            self.eventhandler.pause_until(self.agents_updated())

    def check_time_max(self):
        return self.timer.time < self.timer.end_time

    def agent_end_simulation(self):
        self.end_simulation += 1

    def agents_updated(self):
        for agent in self.agentgroup:
            if not agent.updated:
                return False
        return True
