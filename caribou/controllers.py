"""Controllers."""

import numpy as np
import scipy.linalg
import caribou.solvers as solvers


class LocalController():
    def __init__(self, agentgroup, globalcontroller, plot_callback=None):
        self.agentgroup = agentgroup
        self.globalcontroller = globalcontroller
        self.group_id = self.agentgroup.get_group_id()
        if plot_callback is not None:
            self.plot_calback = plot_callback
        self.control_values = 0

    def generate_random_pv_gen(self):
        raise NotImplementedError

    def run_local_optim(self, globalcontroller_variables):
        x_result, f_result = self.local_solve(globalcontroller_variables)
        self.control_values = x_result
        return x_result, f_result

    def local_solve(self, globalcontroller_variables):
        raise NotImplementedError

    def receive_signal_stop_optimization(self, message=False):
        if message == True:
            self.run_simulation()

    def run_simulation(self):
        raise NotImplementedError


class TravaccaEtAl2017LocalController(LocalController):
    def __init__(self, agentgroup, globalcontroller, plot_callback=None):
        super().__init__(
            agentgroup, globalcontroller, plot_callback=plot_callback)
        self.b = np.genfromtxt('data/travacca_et_al_2017/b.csv', delimiter=',')
        self.e_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max.csv',
            delimiter=',')[self.group_id]
        self.e_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min.csv',
            delimiter=',')[self.group_id]
        self.ev_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max.csv',
            delimiter=',')[self.group_id]
        self.ev_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min.csv',
            delimiter=',')[self.group_id]

        #TODO(Mathilde): Create those matrices and not import them (not flexible)

        self.aeq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/aeq.csv', delimiter=','),
            (1, 48))
        self.aq = np.genfromtxt(
            'data/travacca_et_al_2017/aq.csv', delimiter=',')
        self.beq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/beq.csv', delimiter=','),
            (1, 1))
        self.hq = np.genfromtxt(
            'data/travacca_et_al_2017/hq.csv', delimiter=',')
        self.lbq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/lbq.csv',
                          delimiter=',')[:, self.group_id], (48, 1))
        self.ubq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/ubq.csv',
                          delimiter=',')[:, self.group_id], (48, 1))

    def local_solve(self, globalcontroller_variables):
        mu, nu, day = globalcontroller_variables
        fq = self.create_fq(mu, nu, day)
        new_aq = self.create_new_aq()
        new_bq = self.create_new_bq()
        x_result, f_result = solvers.with_cvxpy(self.hq, fq, new_aq, new_bq,
                                                self.aeq, self.beq)[:2]
        return x_result, f_result

    def create_fq(self, mu, nu, day):
        dam_predict_price = self.globalcontroller.dam_predict_price[day * 24:(day + 1)*24]
        return np.concatenate(
            (dam_predict_price - nu, np.dot(self.b, mu)), axis=0)

#TODO(Mathilde): The two generate functions should be in the mc generator


    def generate_random_pv_gen(self):
        data_pv_gen = self.globalcontroller.pv_gen
        return data_pv_gen + data_pv_gen * (
            np.random.rand(self.globalcontroller.time_horizon * 24) - 0.5)

    def generate_random_load(self):
        data_dam_demand = self.globalcontroller.dam_demand
        return data_dam_demand + data_dam_demand * (
            np.random.rand(self.globalcontroller.time_horizon * 24) - 0.5)

    def create_bq(self):
        data_pv_gen = self.generate_random_pv_gen()
        data_dam_load = self.generate_random_load()
        return np.reshape(
            np.concatenate(
                (self.e_max, -self.e_min, data_pv_gen - data_dam_load),
                axis=0), (72, 1))

    def create_new_aq(self):
        return np.concatenate((self.aq, np.eye(48), -np.eye(48)), axis=0)

    def create_new_bq(self):
        bq = self.create_bq()
        return np.concatenate((bq, self.ubq, -self.lbq), axis=0)

    def run_simulation(self):
        x_result = self.control_values
        g_result = x_result[:24]
        ev_result = x_result[24:]
        print('ok')


# TODO(Mathilde): Create a new module for Global Controller?


class GlobalController():
    def __init__(self, plot_callback=None):
        self.list_localcontrollers = []
        if plot_callback is not None:
            self.plot_callback = plot_callback
        self.day = 0

    def set_list_localcontrollers(self, list_localcontrollers):
        self.list_localcontrollers = list_localcontrollers

    def get_list_localcontrollers(self):
        return self.list_localcontrollers

    def run_global_optim(self):
        self.global_solve()

    def global_solve(self):
        raise NotImplementedError

    def give_signal_stop_optimization(self, message=False):
        for localcontroller in self.list_localcontrollers:
            localcontroller.receive_signal_stop_optimization(message=message)
        self.day += 1


class TravaccaEtAl2017GlobalController(GlobalController):
    def __init__(self, start_day=32, time_horizon=1,
                 plot_callback=None):  # time_horizon in days
        super().__init__(plot_callback=plot_callback)
        self.start_day = start_day
        self.time_horizon = time_horizon
        self.data_main = np.genfromtxt(
            'data/travacca_et_al_2017/main.csv', delimiter=',')
        self.pv_gen = self.load_pv_gen()
        self.b = np.genfromtxt('data/travacca_et_al_2017/b.csv', delimiter=',')
        self.e_max_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max_agg.csv', delimiter=',')
        self.e_min_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min_agg.csv', delimiter=',')
        self.ev_max_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max_agg.csv', delimiter=',')
        self.ev_min_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min_agg.csv', delimiter=',')
        self.c = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/c.csv', delimiter=','),
            (96, 1))
        self.cov_dam_price = self.load_cov_dam_price()
        self.dam_price = self.load_dam_price()
        self.dam_demand = self.load_dam_demand()
        self.dam_predict_price = self.predict_dam_price()

    def load_cov_dam_price(self):
        scale_cov = 1000**2
        return np.genfromtxt(
            'data/travacca_et_al_2017/covariance.csv',
            delimiter=',') / scale_cov

    def load_pv_gen(self):
        start = self.start_day * 4 * 24 + 1
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4
        scale_pv = 10
        return self.data_main[start:stop:4, 16] / scale_pv

    def load_dam_price(self):
        start = self.start_day * 4 * 24 + 1
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4
        scale_price = 1000
        return self.data_main[start:stop:4, 10] / scale_price

    def load_dam_demand(self):
        start = self.start_day * 4 * 24 + 1
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4
        scale_load = 10000
        return self.data_main[start:stop:4, 9] / scale_load

    def predict_dam_price(self):
        dam_predict_price = np.zeros((24 * self.time_horizon, 1))
        for day in range(self.time_horizon):
            product_matrix = np.reshape(
                np.dot(
                    scipy.linalg.sqrtm(self.cov_dam_price),
                    np.random.multivariate_normal(
                        np.zeros((24, )), np.eye(24))), (24, 1))
            matrix_dam_price = np.reshape(
                    self.dam_price[24 * day:24 * (day + 1)], (24, 1))
            dam_predict_price[24 * day:24 * (day + 1)] = matrix_dam_price + product_matrix
        return dam_predict_price

    def global_solve(self, num_iter=50, gamma=0.00001, alpha=1):
        # TODO(Mathilde): verify if list_localcontroller is set. Or find a way to set it automaticaly
        mu, nu, g_result, ev_result, local_optimum_cost, total_cost = self.initialize_gradient_ascent(
            num_iter)
        for i in range(num_iter):
            g_result, ev_result, local_optimum_cost = self.next_step_gradient_ascent(
                mu, nu, g_result, ev_result, local_optimum_cost)
            total_cost[i] = self.compute_total_cost(mu, nu, alpha,
                                                    local_optimum_cost)
            mu = self.update_mu(mu, gamma, ev_result)
            nu = self.update_nu(nu, gamma, alpha, g_result)
        self.plot_callback([np.sum(g_result, axis=1) , np.sum(ev_result, axis=1)],
                           'final load from grid and ev consumption',
                           ['g_result', 'ev_result'])
        self.plot_callback([total_cost], 'total_cost_predicted',
                           ['total cost'])
        self.plot_callback([self.dam_price, self.dam_demand],
                           'DAM prices and energy demand',
                           ['dam_price', 'dam_demand'])
        self.give_signal_stop_optimization(message=True)

    def update_mu(self, mu, gamma, ev_result):
        return np.maximum(mu + gamma * self.c + gamma * np.dot(
            self.b.T, np.reshape(np.sum(ev_result, axis=1), (24, 1))),
                          np.zeros((96, 1)))

    def update_nu(self, nu, gamma, alpha, g_result):
        return nu - gamma * 1 / (2 * alpha) * np.dot(
            np.linalg.inv(self.cov_dam_price), nu) - gamma * np.reshape(
                np.sum(g_result, axis=1).T, (24, 1))

    def compute_total_cost(self, mu, nu, alpha, local_optimum_cost):
        return -1 / (4 * alpha) * np.dot(
            nu.T, np.dot(np.linalg.inv(self.cov_dam_price), nu)) + np.dot(
                self.c.T, mu) + np.sum(local_optimum_cost)

    def initialize_gradient_ascent(self, num_iter):
        size = len(self.list_localcontrollers)
        return np.zeros((96, 1)), np.zeros((24, 1)), np.zeros(
            (24, size)), np.zeros((24, size)), np.zeros((size, 1)), np.zeros(
                (num_iter, 1))

    def next_step_gradient_ascent(self, mu, nu, g_result, ev_result,
                                  local_optimum_cost):
        globalcontroller_variables = (mu, nu, self.day)
        for i, localcontroller in enumerate(self.list_localcontrollers):
            x_result, f_result = localcontroller.run_local_optim(
                globalcontroller_variables)
            g_result[:, i] = x_result[:24]
            ev_result[:, i] = x_result[24:]
            local_optimum_cost[i, 0] = f_result
        return g_result, ev_result, local_optimum_cost
