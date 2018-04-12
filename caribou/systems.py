""" Reference System used for the MC test """

import cvxpy
import numpy as np
import caribou.datagenerators as datagenerators
import sqlite3
import pandas as pd


DATA_PATH = '/Users/mathildebadoual/code/ecoblock_test/data/database.sqlite'

"""
Options =
- aggregate or distributed
- number of batteries with capacity or just capacity
- same for evs, pv
- what is controlled (ev/battery charging/discharing)
- time step we can give a control
- local control of global control
- time step of the simulation
- data
- using a constrained network (congestion)
- add lags for control
- online control with a PID: aggregate or distributed, local or global
- noise added to data given / or not

First Step:
    - aggregate model
    - aggregate number of batteries and PV -> capacity
    - number of EV
    - we can control battery charging and discharging and grid load
    - use aggregate global PID
    - data ecoblock ?

Second Step:
    - aggregate model
    - aggregate number of EV and PV (no batteries)
    - control EV charging
    - use of an aggregate global PID but needs to be correlated with an online MPC (outside of the system)
    - data of the EV probability to come/leave and PV

Third Step:
    - distributed model
    - ...
"""


class System():
    def __init__(self, data_generator=None):
        self.data_generator = data_generator
        if self.data_generator is None:
            self.data_generator = datagenerators.ModelDataGenerator()
        self.set_options()
        self.set_caracteristics()
        self.create_variables()
        self.get_data()
        self.timer = 0

    def set_options(self, time_step=3600, time_control=900, time_simulation=86400, start_date=0, end_date=0):
        self.time_step = time_step
        self.time_control = time_control
        self.time_simulation = time_simulation

        self.start_date = start_date
        self.end_date = end_date
        if start_date != 0:
            self.time_simulation = self.end_date - self.start_date

        self.data_generator.set_time_step(self.time_step)

    def set_caracteristics(self, storage_capacity=480, charging_rate_max=120, discharging_rate_max=120, load_grid_rate_max=120, charging_efficiency=1, discharging_efficiency=1):
        self.storage_capacity = storage_capacity
        self.charging_rate_max = charging_rate_max
        self.discharging_rate_max = discharging_rate_max
        self.load_grid_rate_max = load_grid_rate_max
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency

    def next_step(self):

        self.update_data()

        self.constraints += [self.state_of_charge == self.previous_state_of_charge
                + self.charging_efficiency * self.storage_charging_rate
                - self.discharging_efficiency * self.storage_discharging_rate]
        self.constraints += [self.storage_charging_rate + self.ev_load + self.individual_load == self.storage_discharging_rate + self.load_grid + self.pv_generation]

        cost = cvxpy.Minimize(cvxpy.square(cvxpy.norm(self.y - self.y_objective)))
        problem = cvxpy.Problem(cost, self.constraints)
        problem.solve()

        self.timer += self.time_step

        self.optimization_status = problem.status

        if problem.status == 'optimal':
            return self.y.value

        print(problem.status)
        return None

    def create_variables(self):
        self.previous_state_of_charge = 0

        self.load_grid = cvxpy.Variable(1)
        self.storage_charging_rate = cvxpy.Variable(1)
        self.storage_discharging_rate = cvxpy.Variable(1)
        self.state_of_charge = cvxpy.Variable(1)

        self.y = cvxpy.vstack(self.load_grid, self.storage_charging_rate, self.storage_discharging_rate)

        self.constraints = [0 <= self.state_of_charge,
                self.state_of_charge <= 1]
        self.constraints += [0 <= self.storage_charging_rate,
                self.storage_charging_rate <= self.charging_rate_max]
        self.constraints += [0 <= self.storage_discharging_rate,
                self.storage_discharging_rate <= self.discharging_rate_max]
        self.constraints += [0 <= self.load_grid,
                self.load_grid <= self.load_grid_rate_max]

    def run_simulation(self):
        self.update_data()
        self.state = self.next_step()

    def update_data(self):
        self.y_objective = self.y_objective_datas[self.timer]  #tbd
        self.pv_generation = self.pv_generation_datas[self.timer]
        self.ev_load = self.ev_load_datas[self.timer]
        self.individual_load = self.individual_load_datas[self.timer]

    def get_data(self):
        self.pv_generation_datas = self.data_generator.import_pv_generation()
        self.ev_load_datas = self.data_generator.import_ev_demand()
        self.individual_load_datas = self.data_generator.import_load_demand()
        #this part will be modified with the data generator from Ramon

    def set_y_objective(self, y_objective_datas):
        self.y_objective_datas = y_objective_datas


