""" Agents and Agent States """

import random


class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def get_id(self):
        return self.agent_id


class PV(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.record_gen = []

    def compute_instant_power_gen(self, irradiance):
        self.power_gen = self.efficiency*self.angle*irradiance


class EV(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.capacity = 24
        self.record_soc = []
        self.charge_rate_max = 10
        self.charge_rate_min = -10
        self.charge_rate = 0
        self.state_control = None
        self.actual_state = None

    def set_state_control(self, state_name):
        if state_name in ['gone', 'charging', 'not charging']:
            self.state_control = state_name
        else:
            print('not the right sintax')

    def set_state_actual(self, state_name):
        if state_name in ['gone', 'charging', 'not charging']:
            self.state_actual = state_name
        else:
            print('not the right syntax')

class Battery(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.capacity = 24
        self.record_soc = []
        self.charge_rate_max = 10
        self.charge_rate_min = -10
        self.charge_rate = 0
        self.state_control = None
        self.actual_state = None

    def set_state_control(self, state_name):
        if state_name in ['charging', 'not charging']:
            self.state_control = state_name
        else:
            print('not the right syntax')

    def set_state_actual(self, state_name):
        if state_name in ['charging', 'not charging']:
            self.state_actual = state_name
        else:
            print('not the right sintax')




# TODO(Mathilde): this part should be somewhere else because it is the model of the agents

class State:
    def __init__(self, agent, name, eventhandler, localcontroller, transition_dict):
        self.agent = agent
        self.name = name
        self.eventhander = eventhandler
        self.localcontroller
        self.transition_dict = transition_dict
        self.reachable_states = self.transition_dict[self]

    def check_transition_from(self):
        for state in self.reachable_states:
            if state[1](self.y_current, self.agent):
                self.state_to_transit = state[0]
                return True
        return False

    def run_step(self):
        raise NotImplementedError

    def run_sim(self, y_init):
        raise NotImplementedError


class EvState:
    def __init__(self, agent, name, eventhandler, localcontroller, transition_dict, charge_on):
        super().__init__(agent, name, eventhandler, localcontroller, transition_dict)
        self.charge_on = charge_on

    def run_step(self):
        return self.y_current + self.charge_on * self.agent.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        self.agent.actual_state = self.name
        if self.name == 'gone':
            self.y_current = random.randint(0, self.agent.capacity)
        while not self.check_transition_from and self.local_controller.check_time_max():
            self.eventhandler.pause_until(self.localcontroller.updated)
            self.y_current = self.run_step()
            self.agent.record_soc.append(self.y_current)
        if not self.local_controller.check_time_max():
            self.local_controller.agent_end_simulation()
        return self.state_to_transit.run_sim(self.y_current)


class BatteryState:
    def __init__(self, agent, name, eventhandler, localcontroller, transition_dict, charge_on):
        super().__init__(agent, name, eventhandler, localcontroller, transition_dict)
        self.charge_on = charge_on

    def run_step(self):
        return self.y_current + self.charge_on * self.agent.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        self.agent.actual_state = self.name
        while not self.check_transition_from and self.local_controller.check_time_max():
            self.eventhandler.pause_until(self.localcontroller.updated)
            self.y_current = self.run_step()
            self.agent.record_soc.append(self.y_current)
        if not self.local_controller.check_time_max():
            self.local_controller.agent_end_simulation()
        return self.state_to_transit.run_sim(self.y_current)


# transition functions:

def t_ev_not_charge(y, agent):
    if (y == agent.capacity or y == 0) and not agent.state_control == 'gone':
        return True
    if agent.state_control == 'not charge':
        return True
    return False

def t_ev_charge(y, agent):
    if agent.state_control == 'charge':
        return True
    return False

def t_ev_gone(y, agent):
    if agent.state_control == 'gone':
        return True
    return False

def t_b_not_charge(y, agent):
    if (y == agent.capacity or y == 0):
        return True
    if agent.state_control == 'not charge':
        return True
    return False

def t_b_charge(y, agent):
    if agent.state_control == 'charge':
        return True
    return False

