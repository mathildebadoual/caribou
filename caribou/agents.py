""" Agents and Agent States """

import random


class Agent:
    def __init__(self, agent_id, localcontroller):
        self.agent_id = agent_id
        self.localcontroller = localcontroller

    def get_id(self):
        return self.agent_id


class EV(Agent):
    def __init__(self, agent_id, localcontroller):
        super().__init__(agent_id, localcontroller)
        self.capacity = 24
        self.record_soc = []
        self.charge_rate_max = 10
        self.charge_rate_min = -10
        self.charge_rate = 0
        self.status_control = None
        self.status_current = None
        self.build_state_machine()

    def build_state_machine(self):
        self.charge = EvState(self, 'charge', self.localcontroller, 1)
        self.not_charge = EvState(self, 'not charge', self.localcontroller, 0)
        self.gone = EvState(self, 'gone', self.localcontroller, 0)
        self.transition_dict = {
                self.charge: [[self.not_charge, self.t_ev_not_charge], [self.gone, self.t_ev_gone]],
                self.not_charge: [[self.charge, self.t_ev_charge], [self.gone, self.t_ev_gone]],
                self.gone: [[self.charge, self.t_ev_charge], [self.not_charge, self.t_ev_not_charge]]}

    def t_ev_not_charge(self, y):
        if (y == agent.capacity or y == 0) and not self.status_control == 'gone':
            return True
        if self.status_control == 'not charge':
            return True
        return False

    def t_ev_charge(self, y):
        if self.status_control == 'charge':
            return True
        return False

    def t_ev_gone(self, y):
        if self.status_control == 'gone':
            return True
        return False

    def set_status_control(self, state_name):
        if state_name in ['gone', 'charging', 'not charging']:
            self.status_control = state_name
        else:
            print('not the right sintax')

    def set_status_current(self, state_name):
        if state_name in ['gone', 'charging', 'not charging']:
            self.status_current = state_name
        else:
            print('not the right syntax')


class Battery(Agent):
    def __init__(self, agent_id, localcontroller):
        super().__init__(agent_id, localcontroller)
        self.capacity = 24
        self.record_soc = []
        self.charge_rate_max = 10
        self.charge_rate_min = -10
        self.charge_rate = 0
        self.status_control = None
        self.status_current = None
        self.build_state_machine()

    def build_state_machine(self):
        self.charge = BatteryState(self, 'charge', self.localcontroller, 1)
        self.not_charge = BatteryState(self, 'not charge', self.localcontroller, 0)
        self.transition_dict = {
                self.charge : [[self.not_charge, self.t_b_not_charge]],
                self.not_charge : [[self.charge, self.t_b_charge]]}

    def t_b_not_charge(self, y):
        if (y == self.capacity or y == 0):
            return True
        if self.status_control == 'not charge':
            return True
        return False

    def t_b_charge(self, y):
        if self.status_control == 'charge':
            return True
        return False

    def set_status_control(self, state_name):
        if state_name in ['charging', 'not charging']:
            self.status_control = state_name
        else:
            print('not the right syntax')

    def set_status_current(self, state_name):
        if state_name in ['charging', 'not charging']:
            self.status_current = state_name
        else:
            print('not the right sintax')




# TODO(Mathilde): this part should be somewhere else because it is the model of the agents

class State:
    def __init__(self, agent, name, localcontroller):
        self.agent = agent
        self.name = name
        self.eventhander = localcontroller.eventhandler
        self.localcontroller = localcontroller

    def check_transition_from(self):
        reachable_states = self.agent.transition_dict[self]
        for state in reachable_states:
            if state[1](self.y_current, self.agent):
                self.state_to_transit = state[0]
                return True
        return False

    def run_step(self):
        raise NotImplementedError

    def run_sim(self, y_init):
        raise NotImplementedError


class EvState(State):
    def __init__(self, agent, name, localcontroller, charge_on):
        super().__init__(agent, name, localcontroller)
        self.charge_on = charge_on

    def run_step(self):
        return self.y_current + self.charge_on * self.agent.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        self.agent.status_current = self.name
        if self.name == 'gone':
            self.y_current = random.randint(0, self.agent.capacity)
        while not self.check_transition_from and self.local_controller.check_time_max():
            self.eventhandler.pause_until(self.localcontroller.updated)
            self.y_current = self.run_step()
            self.agent.record_soc.append(self.y_current)
        if not self.local_controller.check_time_max():
            self.local_controller.agent_end_simulation()
        return self.state_to_transit.run_sim(self.y_current)


class BatteryState(State):
    def __init__(self, agent, name, localcontroller, charge_on):
        super().__init__(agent, name, localcontroller)
        self.charge_on = charge_on

    def run_step(self):
        return self.y_current + self.charge_on * self.agent.charge_rate

    def run_sim(self, y_init):
        self.y_current = y_init
        self.agent.status_current = self.name
        while not self.check_transition_from and self.local_controller.check_time_max():
            self.eventhandler.pause_until(self.localcontroller.updated)
            self.y_current = self.run_step()
            self.agent.record_soc.append(self.y_current)
        if not self.local_controller.check_time_max():
            self.local_controller.agent_end_simulation()
        return self.state_to_transit.run_sim(self.y_current)
