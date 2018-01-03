"""Controllers."""

import numpy as np
import scipy.linalg
import quadprog


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
        self.identity = self.id_generator
        self.id_generator += 1

    def local_solve(self, globalcontroller_variables):
        mu, nu = globalcontroller_variables

        b = self.load_b_matrix()
        dam_predict_price = self.globalcontroller.predict_dam_price()
        f = np.array(dam_predict_price - nu, np.dot(b, mu))

        h = self.load_hq()
        a = self.create_new_aq()
        ae = self.load_aeq()
        b = self.create_new_bq()
        be = self.load_beq()

        x_result, f_result = self.solve_with_quadprog(h, f, a, ae, b, be)
        self.g_result = x_result[:24]
        self.ev_result = x_result[24:]
        return x_result, f_result

# TODO(Mathilde): create a class with all the solvers modified like this one

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
            a_qp = -np.vstack([ae, a]).T
            b_qp = -np.hstack([be, b])
            meq = ae.shape[0]
        else:
            a_qp = -a.T
            b_qp = -b
            meq = 0
        return quadprog.solve_qp(h_qp, f_qp, a_qp, b_qp, meq)


# TODO(Mathilde): Create a class load or put the load functions outside of classes + permit more than 100 houses by building those matrices in the code

    def load_b(self):
        return np.genfromtxt('data/travacca_et_al_2017/b.csv', delimiter=',')

    def load_e_max(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max.csv',
            delimiter=',')[self.identity]

    def load_e_min(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min.csv',
            delimiter=',')[self.identity]

    def load_ev_max(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max.csv',
            delimiter=',')[self.identity]

    def load_ev_min(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min.csv',
            delimiter=',')[self.identity]

    def load_aeq(self):
        return np.genfromtxt('data/travacca_et_al_2017/aeq.csv', delimiter=',')

    def load_aq(self):
        return np.genfromtxt('data/travacca_et_al_2017/aq.csv', delimiter=',')

    def load_beq(self):
        return np.genfromtxt('data/travacca_et_al_2017/beq.csv', delimiter=',')

    def load_hq(self):
        return np.genfromtxt('data/travacca_et_al_2017/hq.csv', delimiter=',')

    def load_lbq(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/lbq.csv',
            delimiter=',')[:, self.identity]

    def load_ubq(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/ubq.csv',
            delimiter=',')[:, self.identity]

    def generate_random_pv_gen(self):
        data_pv_gen = self.globalcontroller.load_pv_gen()
        return data_pv_gen + data_pv_gen * (
            np.random.rand(self.globalcontroller.time_horizon * 24) - 0.5)

    def generate_random_load(self):
        data_dam_demand = self.globalcontroller.load_dam_demand()
        return data_dam_demand + data_dam_demand * (
            np.random.rand(self.globalcontroller.time_horizon * 24) - 0.5)

    def create_bq(self):
        dam_e_max = self.load_e_max()
        dam_e_min = self.load_e_min()
        data_pv_gen = self.generate_random_pv_gen()
        data_dam_load = self.generate_random_load()
        return np.concatenate(
            (dam_e_max, -dam_e_min, data_pv_gen - data_dam_load), axis=0)

    def create_new_aq(self):
        aq = self.load_aq()
        return np.concatenate((aq, np.eye(48), -np.eye(48)), axis=0)

    def create_new_bq(self):
        ubq = self.load_ubq()
        lbq = self.load_lbq()
        bq = self.create_bq()
        return np.concatenate((bq, ubq, -lbq), axis=0)


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
    def __init__(self, start_day=2, time_horizon=1):  # time_horizon in days
        super().__init__()
        self.start_day = start_day
        self.time_horizon = time_horizon
        self.data_main = np.genfromtxt(
            'data/travacca_et_al_2017/main.csv', delimiter=',')

    def load_pv_gen(self):
        start = self.start_day * 4 * 24
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4 - 1
        scale_pv = 10
        return self.data_main[start:stop:4, 16] / scale_pv

    def load_e_max_agg(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max_agg.csv', delimiter=',')

    def load_e_min_agg(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min_agg.csv', delimiter=',')

    def load_ev_max_agg(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max_agg.csv', delimiter=',')

    def load_ev_min_agg(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min_agg.csv', delimiter=',')

    def load_c(self):
        return np.genfromtxt('data/travacca_et_al_2017/c.csv', delimiter=',')

    def load_dam_price(self):
        start = self.start_day * 4 * 24
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4 - 1
        scale_price = 1000
        return self.data_main[start:stop:4, 11] / scale_price

    def load_dam_demand(self):
        start = self.start_day * 4 * 24
        stop = self.start_day * 4 * 24 + self.time_horizon * 24 * 4 - 1
        scale_load = 10000
        return self.data_main[start:stop:4, 10] / scale_load

    def load_cov_dam_price(self):
        return np.genfromtxt(
            'data/travacca_et_al_2017/covariance.csv', delimiter=',')

    def predict_dam_price(self):
        cov_dam_price = self.load_cov_dam_price()
        dam_price = self.load_dam_price()
        dam_predict_price = np.zeros((24, self.time_horizon))
        for day in range(self.time_horizon):
            product_matrix = np.reshape(
                np.dot(
                    scipy.linalg.sqrtm(cov_dam_price),
                    np.random.multivariate_normal(
                        np.zeros((24, )), np.eye(24))), (24, 1))
            matrix_dam_price = np.reshape(
                dam_price[24 * (day - 1):24 * (day + 1)], (24, 1))
            dam_predict_price[24 * day:24 * (
                day + 1), :] = matrix_dam_price + product_matrix
        return dam_predict_price

    def global_solve(self, num_iter=50, gamma=0.00001, alpha=1):
        mu, nu, g_result, ev_result, local_optimum_cost, total_cost = self.initialize_gradient_accent(
            self, num_iter)
        for i in range(num_iter):
            g_result, ev_result, local_optimum_cost = self.next_step_gradiant_accent(
                mu, nu, g_result, ev_result, local_optimum_cost)
            total_cost[i] = self.compute_total_cost(mu, nu, alpha, local_optimum_cost)

    def compute_total_cost(self, mu, nu, alpha, local_optimum_cost):
        cov_dam_price = self.load_cov_dam_price()
        c = self.load_c()
        return -1 / (4 * alpha) * np.dot(
            nu.T, np.dot(np.linalg.inv(cov_dam_price), nu)) + np.dot(
                c.T, mu) + np.sum(local_optimum_cost)

    def initialize_gradient_accent(self, num_iter):
        size = len(self.list_localcontrollers)
        return np.zeros((96, 1)), np.zeros((24, 1)), np.zeros(
            (24, size)), np.zeros((24, size)), np.zeros((size, 1)), np.zeros(
                (num_iter, 1))

    def next_step_gradient_accent(self, mu, nu, g_result, ev_result,
                                  local_optimum_cost):
        globalcontroller_variables = (mu, nu)
        for i, localcontroller in enumerate(self.list_localcontrollers):
            x_result, f_result = localcontroller.run_local_optim(
                globalcontroller_variables)
            g_result[:, i] = x_result[:24]
            ev_result[:, i] = x_result[24:]
            local_optimum_cost[i, 0] = f_result
        return g_result, ev_result, local_optimum_cost
