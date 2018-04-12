""" Agents"""

import numpy as np


class Agent:
    def __init__(self, agent_id, localcontroller):
        self.agent_id = agent_id
        self.localcontroller = localcontroller
        self.updated = False

    def get_id(self):
        return self.agent_id


class ElectricVehicle(Agent):
    def __init__(self):
        pass


class Storage(Agent):
    def __init__(self, capacity=480, charging_rate_max_hour=120, discharging_rate_max_hour=120):
        self.capacity = capacity
        self.charging_rate_max_in_hour = charging_rate_max_hour
        self.discharging_rate_max_in_hour = discharging_rate_max_hour


    def is_full(self):
        return sum(self.soc_record) >= self.capacity

    def is_empty(self):
        return sum(self.soc_record) <= 0

    def charge(self, energy, index):
        if not self.is_full():
            if (self.capacity - sum(self.soc_record)) >= energy:
                if self.charging_rate_max_in_hour >= energy:
                    self.soc_record[index] += energy
                else:
                    self.soc_record[index] += self.charging_rate_max_in_hour
                    self.eventhandler.load_to_grid[index] += energy - self.charging_rate_max_in_hour
            else:
                energy_enabled = self.capacity - sum(self.soc_record)
                if self.charging_rate_max_in_hour >= energy_enabled:
                    self.soc_record[index] += energy_enabled
                else:
                    self.soc_record[index] += self.charging_rate_max_in_hour
                    self.eventhandler.load_to_grid[index] += energy_enabled - self.charging_rate_max_in_hour
                self.eventhandler.load_to_grid[index] += energy - energy_enabled

    def discharge(self, energy, index): #energy needs to be > 0
        if not self.is_empty():
            if sum(self.soc_record) >= energy:
                if self.discharging_rate_max_in_hour >= energy:
                    self.soc_record[index] += - energy
                else:
                    self.soc_record[index] += self.discharging_rate_max_in_hour
                    self.eventhandler.load_from_grid[index] += energy - self.discharging_rate_max_in_hour
            else:
                energy_enabled = sum(self.soc_record)
                if self.discharging_rate_max_in_hour >= energy_enabled:
                    self.soc_record[index] += - energy_enabled
                else:
                    self.soc_record[index] += self.discharging_rate_max_in_hour
                    self.eventhandler.load_from_grid[index] += - energy_enabled + self.discharging_rate_max_in_hour
                self.eventhandler.load_from_grid[index] += - energy + energy_enabled


