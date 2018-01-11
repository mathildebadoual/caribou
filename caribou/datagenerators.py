"""generator of random variables for the Monte Carlo Simulation"""

import numpy as np
import scipy.linalg


PV_GEN_COLUMN = 16
HOURS_PER_DAY = 24
VALUES_PER_DAY = HOURS_PER_DAY * 4


class DataGenerator():
    def __init__(self):
        pass


# TODO(Mathilde): initialize the random seed ?


class TravaccaEtAl2017DataGenerator(DataGenerator):
    def __init__(self, start_day, time_horizon):
        super().__init__()
        self.start_day = start_day
        self.time_horizon = time_horizon
        self.data_main = np.genfromtxt(
            'data/travacca_et_al_2017/main.csv', delimiter=',')
        self.pv_gen = self.load_pv_gen()
        self.e_max_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max_agg.csv', delimiter=',')
        self.e_min_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min_agg.csv', delimiter=',')
        self.ev_max_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max_agg.csv', delimiter=',')
        self.ev_min_agg = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min_agg.csv', delimiter=',')
        self.cov_dam_price = self.load_cov_dam_price()
        self.dam_price = self.load_dam_price()
        self.dam_demand = self.load_dam_demand()
        self.dam_predict_price = self.load_predict_dam_price()
        self.e_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_max.csv', delimiter=',')
        self.e_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_e_min.csv', delimiter=',')
        self.ev_max = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_max.csv', delimiter=',')
        self.ev_min = np.genfromtxt(
            'data/travacca_et_al_2017/dam_EV_min.csv', delimiter=',')
        self.dam_price_predicted = self.load_predict_dam_price()
        np.savetxt('pv_gen_ind.csv', self.generate_random_individual_pv_gen(0), delimiter=',')
        np.savetxt('load_ind.csv', self.generate_random_individual_load(0), delimiter=',')

    def load_pv_gen(self):
        start = self.start_day * VALUES_PER_DAY + 1
        stop = (self.start_day + self.time_horizon) * VALUES_PER_DAY
        scale_pv = 10
        return self.data_main[start:stop:4, PV_GEN_COLUMN] / scale_pv

    def generate_random_individual_pv_gen(self, day):
        pv_gen_day = self.pv_gen[day * HOURS_PER_DAY:(day + 1) * HOURS_PER_DAY]
        return np.reshape(pv_gen_day * (
            0.5 + np.random.rand(self.time_horizon * HOURS_PER_DAY)), (-1, 1))

    def generate_random_individual_load(self, day):
        load_day = self.dam_demand[day * HOURS_PER_DAY:(
            day + 1) * HOURS_PER_DAY]
        return np.reshape(load_day * (
            0.5 + np.random.rand(self.time_horizon * HOURS_PER_DAY)), (-1, 1))

    def load_cov_dam_price(self):
        scale_cov = 1000 ** 2
        return np.genfromtxt(
            'data/travacca_et_al_2017/covariance.csv',
            delimiter=',') / scale_cov

    def load_dam_price(self):
        start = self.start_day * VALUES_PER_DAY + 1
        stop = self.start_day * VALUES_PER_DAY + self.time_horizon * VALUES_PER_DAY
        scale_price = 1000
        return self.data_main[start:stop:4, 10] / scale_price

    def load_dam_demand(self):
        start = self.start_day * VALUES_PER_DAY + 1
        stop = self.start_day * VALUES_PER_DAY + self.time_horizon * VALUES_PER_DAY
        scale_load = 10000
        return self.data_main[start:stop:4, 9] / scale_load


# TODO(Mathilde): Maybe have another module for prediction later

    def load_predict_dam_price(self):
        dam_predict_price = np.zeros((HOURS_PER_DAY * self.time_horizon, 1))
        for day in range(self.time_horizon):
            product_matrix = np.reshape(
                np.dot(
                    scipy.linalg.sqrtm(self.cov_dam_price),
                    np.random.multivariate_normal(
                        np.zeros((HOURS_PER_DAY, )), np.eye(HOURS_PER_DAY))),
                (-1, 1))
            matrix_dam_price = np.reshape(
                self.dam_price[HOURS_PER_DAY * day:HOURS_PER_DAY * (day + 1)],
                (-1, 1))
            dam_predict_price[HOURS_PER_DAY * day:HOURS_PER_DAY * (
                day + 1)] = matrix_dam_price + product_matrix
        return dam_predict_price

    def load_individual_e_max(self, group_id):
        return np.reshape(self.e_max[group_id, :], (1, HOURS_PER_DAY))

    def load_individual_e_min(self, group_id):
        return np.reshape(self.e_min[group_id, :], (1, HOURS_PER_DAY))

    def load_individual_ev_max(self, group_id):
        return np.reshape(self.ev_max[group_id, :], (1, HOURS_PER_DAY))

    def load_individual_ev_min(self, group_id):
        return np.reshape(self.ev_min[group_id, :], (1, HOURS_PER_DAY))

    def load_individual_dam_price_predicted(self, day):
        return np.reshape(self.load_predict_dam_price()[day * HOURS_PER_DAY:(
            24 + 1) * HOURS_PER_DAY], (-1, 1))
