""" Agents and Agent States """

import random


class Agent:
    def __init__(self, agent_id, localcontroller):
        self.agent_id = agent_id
        self.localcontroller = localcontroller
        self.updated = False

    def get_id(self):
        return self.agent_id


class EV(Agent):



class Battery(Agent):
    def __init__(self, agent_id, localcontroller):
