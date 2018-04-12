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
    def __init__(self, data_generator=None, plot_callback=None):
        self.data_generator = data_generator
        if self.data_generator is None:
            self.data_generator = datagenerators.ModelDataGenerator()
        self.set_options()
        self.set_caracteristics()
        self.previous_state_of_charge = 0
        self.get_data()
        self.timer = 0
        if plot_callback is None:
            self.plot_callback = plot_callback

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

        load_grid = cvxpy.Variable()
        storage_charging_rate = cvxpy.Variable()
        storage_discharging_rate = cvxpy.Variable()
        state_of_charge = cvxpy.Variable()

        y = cvxpy.vstack(load_grid, storage_charging_rate, storage_discharging_rate)

        constraints = [0 <= state_of_charge,
                state_of_charge <= 1]
        constraints += [0 <= storage_charging_rate,
                storage_charging_rate <= self.charging_rate_max]
        constraints += [0 <= storage_discharging_rate,
                storage_discharging_rate <= self.discharging_rate_max]
        constraints += [0 <= load_grid,
                load_grid <= self.load_grid_rate_max]

        constraints += [state_of_charge == self.previous_state_of_charge + storage_charging_rate - storage_discharging_rate]
        constraints += [storage_charging_rate + self.ev_load + self.individual_load == storage_discharging_rate + load_grid + self.pv_generation]
        constraints += [storage_charging_rate >= 0, storage_discharging_rate >= 0]

        cost = cvxpy.Minimize(cvxpy.square(cvxpy.norm(y - self.y_objective)))
        problem = cvxpy.Problem(cost, constraints)
        problem.solve()

        self.timer += self.time_step

        self.optimization_status = problem.status
        self.previous_state_of_charge = state_of_charge.value

        if problem.status == 'optimal':
            state = np.concatenate((y.value, np.array([[state_of_charge.value]])), axis=0)
            print(state)
            return state

        print(problem.status)
        return None

    def run_simulation(self):
        self.states_memory = np.zeros((4, int(self.time_simulation/self.time_step)))
        for step in range(int(self.time_simulation/self.time_step)):
            self.state = self.next_step()
            self.states_memory[:, step] = np.reshape(self.state, (-1))

    def update_data(self):
        index = int(self.timer/3600)
        print(index)
        self.y_objective = self.y_objective_datas[:, index]
        self.pv_generation = self.pv_generation_datas[index]
        self.ev_load = self.ev_load_datas[index]
        self.individual_load = self.individual_load_datas[index]
        print(self.pv_generation)
        print(self.ev_load)
        print(self.individual_load)

    def get_data(self):
        self.pv_generation_datas = self.data_generator.import_pv_generation()
        self.ev_load_datas = self.data_generator.import_ev_demand()
        self.individual_load_datas = self.data_generator.import_load_demand()
        #this part will be modified with the data generator from Ramon

    def set_y_objective(self, y_objective_datas):
        self.y_objective_datas = y_objective_datas

    def plot_results(self):
        self.plot_callback(self.states_memory.T, 'plot_test', ['load_grid', 'storage_charging_rate', 'storage_discharging_rate', 'soc'])
