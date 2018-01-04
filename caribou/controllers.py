"""Controllers."""

import numpy as np
import scipy.linalg
import quadprog
import caribou.callback as callback

np.random.seed(seed=1)
callbackplot = callback.CallBackPlot()

class Controller:
    def __init__(self):
        pass


class LocalController(Controller):
    id_generator = 0

    def __init__(self, agentgroup, globalcontroller):
        super().__init__()
        self.agentgroup = agentgroup
        self.globalcontroller = globalcontroller

    def generate_random_pv_gen(self):
        raise NotImplementedError

    def run_local_optim(self, globalcontroller_variables):
        x_result, f_result = self.local_solve(globalcontroller_variables)
        return x_result, f_result

    def local_solve(self, globalcontroller_variables):
        raise NotImplementedError


class TravaccaEtAl2017LocalController(LocalController):
    def __init__(self, agentgroup, globalcontroller):
        super().__init__(agentgroup, globalcontroller)
        self.identity = LocalController.id_generator
        LocalController.id_generator += 1
        self.b = np.genfromtxt('data/travacca_et_al_2017/b.csv', delimiter=',')
        self.e_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max.csv',
            delimiter=',')[self.identity]
        self.e_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min.csv',
            delimiter=',')[self.identity]
        self.ev_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max.csv',
            delimiter=',')[self.identity]
        self.ev_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min.csv',
            delimiter=',')[self.identity]
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
                          delimiter=',')[:, self.identity], (48, 1))
        self.lbq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/lbq.csv',
                          delimiter=',')[:, self.identity], (48, 1))
        self.ubq = np.reshape(
            np.genfromtxt('data/travacca_et_al_2017/ubq.csv',
                          delimiter=',')[:, self.identity], (48, 1))

    def local_solve(self, globalcontroller_variables):
        mu, nu = globalcontroller_variables
        fq = self.create_fq(mu, nu)
        new_aq = self.create_new_aq()
        new_bq = self.create_new_bq()

        print(self.identity)

        x_result, f_result = self.solve_with_quadprog(
            self.hq, fq, new_aq, new_bq, self.aeq, self.beq)[:2]
        self.g_result = x_result[:24]
        self.ev_result = x_result[24:]
        return x_result, f_result

    def solve_with_quadprog(self, h, f, a, b, ae, be):
        """
        Solve the following quadratic programm using quadprog:

        minimize
             (1/2) * x.T * h * x + f.T * x

        subject to
             a * x <= b
             ae * x == be
        """
        h_qp = h
        f_qp = -f
        if ae is not None:
            a_qp = -np.concatenate((ae, a), axis=0).T
            b_qp = -np.concatenate((be, b), axis=0)
            meq = ae.shape[0]
        else:
            a_qp = -a.T
            b_qp = -b
            meq = 0
        b_qp = np.reshape(b_qp, (b_qp.shape[0], ))
        f_qp = np.reshape(f_qp, (f_qp.shape[0], ))
        return quadprog.solve_qp(h_qp, f_qp, a_qp, b_qp, meq)

    def create_fq(self, mu, nu):
        dam_predict_price = self.globalcontroller.predict_dam_price()
        return np.concatenate(
            (dam_predict_price - nu, np.dot(self.b, mu)), axis=0)

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
        callbackplot.add([data_pv_gen, data_dam_load], 'pv_gen and dam_load for each individual')
        return np.reshape(
            np.concatenate(
                (self.e_max, -self.e_min, data_pv_gen - data_dam_load),
                axis=0), (72, 1))

    def create_new_aq(self):
        return np.concatenate((self.aq, np.eye(48), -np.eye(48)), axis=0)

    def create_new_bq(self):
        bq = self.create_bq()
        return np.concatenate((bq, self.ubq, -self.lbq), axis=0)


class GlobalController(Controller):
    def __init__(self):
        super().__init__()
        self.list_localcontrollers = []

    def set_list_localcontrollers(self, list_localcontrollers):
        self.list_localcontrollers = list_localcontrollers

    def get_list_localcontrollers(self):
        return self.list_localcontrollers

    def run_global_optim(self):
        self.global_solve()

    def global_solve(self):
        raise NotImplementedError


class TravaccaEtAl2017GlobalController(GlobalController):
    def __init__(self, start_day=32, time_horizon=1):  # time_horizon in days
        super().__init__()
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
        self.cov_dam_price = np.genfromtxt(
            'data/travacca_et_al_2017/covariance.csv', delimiter=',')
        self.dam_price = self.load_dam_price()
        self.dam_demand = self.load_dam_demand()
        callbackplot.add([self.dam_price, self.dam_demand], 'dam_price and dam_demand')

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
        dam_predict_price = np.zeros((24, self.time_horizon))
        for day in range(self.time_horizon):
            product_matrix = np.reshape(
                np.dot(
                    scipy.linalg.sqrtm(self.cov_dam_price),
                    np.random.multivariate_normal(
                        np.zeros((24, )), np.eye(24))), (24, 1))
            matrix_dam_price = np.reshape(
                self.dam_price[24 * (day - 1):24 * (day + 1)], (24, 1))
            dam_predict_price[24 * day:24 * (
                day + 1), :] = matrix_dam_price + product_matrix
        return dam_predict_price

    def global_solve(self, num_iter=2, gamma=0.00001, alpha=1):
        # TODO(Mathilde): verify if list_localcontroller is set. Or find a way to set it automaticaly
        mu, nu, g_result, ev_result, local_optimum_cost, total_cost = self.initialize_gradient_ascent(
            num_iter)
        for i in range(num_iter):
            g_result, ev_result, local_optimum_cost = self.next_step_gradient_ascent(
                mu, nu, g_result, ev_result, local_optimum_cost)
            total_cost[i] = self.compute_total_cost(mu, nu, alpha,
                                                    local_optimum_cost)
            mu = self.update_mu(mu, gamma, ev_result)
            nu - self.update_nu(nu, gamma, alpha, g_result)
            print('mu=', mu)
            print('nu=', nu)
            callbackplot.add([np.sum(g_result, axis=1), np.sum(ev_result, axis=1)], 'results of global_solve')

    def update_mu(self, mu, gamma, ev_result):
        return max(mu + gamma * self.c + gamma * np.dot(
            self.b.T, np.reshape(np.sum(ev_result, axis=1), (24, 1))), 0)

    def update_nu(self, nu, gamma, alpha, g_result):
        return nu - gamma * 1 / (2 * alpha) * np.dot(
            np.linalg.inv(self.cov_dam_price), nu) - gamma * np.reshape(
                np.sum(g_result, axis=1), (24, 1))

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
        globalcontroller_variables = (mu, nu)
        for i, localcontroller in enumerate(self.list_localcontrollers):
            x_result, f_result = localcontroller.run_local_optim(
                globalcontroller_variables)
            g_result[:, i] = x_result[:24]
            ev_result[:, i] = x_result[24:]
            local_optimum_cost[i, 0] = f_result

        return g_result, ev_result, local_optimum_cost

callbackplot.plot_all()
