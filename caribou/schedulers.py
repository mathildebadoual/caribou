"""Schedulers for"""

import numpy as np
import cvxpy
import caribou.datagenerators as datagenerators
import caribou.solvers as solvers

HOURS_PER_DAY = 24


""" Loval Schedulers """


class LocalScheduler():
    def __init__(self,
                 agentgroup,
                 globalscheduler,
                 plot_callback=None):
        self.agentgroup = agentgroup
        self.globalscheduler = globalscheduler
        self.group_id = self.agentgroup.get_group_id()
        if plot_callback is not None:
            self.plot_calback = plot_callback
        self.control_values = 0

    def local_solve(self, globalscheduler_variables):
        raise NotImplementedError


class ModelLocalScheduler(LocalScheduler):
    def __init__(self,
            agentgroup,
            globalscheduler,
            data_generator,
            plot_callback=None):
        super().__init__(
                agentgroup, globalscheduler, plot_callback=plot_callback)


class TravaccaEtAl2017AggLocalScheduler(LocalScheduler):
    def __init__(self,
            agentgroup,
            globalscheduler,
            data_generator,
            plot_callback=None):
        super().__init__(
                agentgroup, globalscheduler, plot_callback=plot_callback)


class TravaccaEtAl2017LocalScheduler(LocalScheduler):
    def __init__(self,
                 agentgroup,
                 globalscheduler,
                 data_generator,
                 plot_callback=None):
        super().__init__(
            agentgroup, globalscheduler, plot_callback=plot_callback)

        self.data_generator = data_generator
        self.delta = 0.01
        self.max_local_power = 10

        self.e_max = self.data_generator.load_individual_e_max(self.group_id)
        self.e_min = self.data_generator.load_individual_e_min(self.group_id)
        self.ev_max = self.data_generator.load_individual_ev_max(self.group_id)
        self.ev_min = self.data_generator.load_individual_ev_min(self.group_id)

    def run_local_optim(self, globalscheduler_variables, solver=None):
        if solver is None:
            x_result, f_result = self.local_solve(globalscheduler_variables)
        if solver is not None:
            x_result, f_result = self.local_solve(
                globalscheduler_variables, solver=solver)

        self.grid_load_result = x_result[:HOURS_PER_DAY]
        self.ev_load_result = x_result[HOURS_PER_DAY:]

        return x_result, f_result

    def update_matrices_local_quadr_opt(self, day):
        self.individual_dam_price_predicted = self.data_generator.load_individual_dam_price_predicted(day)
        self.individual_pv_gen_predicted = self.data_generator.generate_random_individual_pv_gen(day)
        self.individual_load_predicted = self.data_generator.generate_random_individual_load(day)
        self.aeq = np.zeros((1, 2 * HOURS_PER_DAY))
        self.beq = np.array([[0]])
        self.aq = self.create_aq()
        self.hq = self.delta * np.eye(2 * HOURS_PER_DAY)
        self.lbq = self.create_lbq()
        self.ubq = self.create_ubq()
        self.bq = self.create_bq()

    def create_ubq(self):
        return np.concatenate(
            (self.max_local_power * np.ones(
                (HOURS_PER_DAY, 1)), self.ev_max.T),
            axis=0)

    def create_lbq(self):
        return np.concatenate(
            (-self.max_local_power * np.ones(
                (HOURS_PER_DAY, 1)), self.ev_min.T),
            axis=0)

    def create_aq(self):
        a = np.tril(np.ones((HOURS_PER_DAY, HOURS_PER_DAY)))
        matrix_a = np.concatenate(
            (np.zeros(
                (2 * HOURS_PER_DAY, HOURS_PER_DAY)), -np.eye(HOURS_PER_DAY)),
            axis=0)
        matrix_b = np.concatenate((a, -a, np.eye(HOURS_PER_DAY)), axis=0)
        matrix_ab = np.concatenate((matrix_a, matrix_b), axis=1)
        return np.concatenate(
            (matrix_ab, np.eye(2 * HOURS_PER_DAY), -np.eye(2 * HOURS_PER_DAY)),
            axis=0)

    def create_bq(self):
        bq = np.reshape(
            np.concatenate(
                (self.e_max.T, - self.e_min.T, self.individual_pv_gen_predicted -
                 self.individual_load_predicted),
                axis=0), (-1, 1))
        return np.concatenate((bq, self.ubq, -self.lbq), axis=0)

    def update_fq(self, mu, nu, day):
        a = np.tril(np.ones((HOURS_PER_DAY, HOURS_PER_DAY)))
        b = np.concatenate(
            (-a.T, a.T, -np.eye(HOURS_PER_DAY), np.eye(HOURS_PER_DAY)), axis=1)
        return np.concatenate(
            (self.individual_dam_price_predicted - nu, np.dot(b, mu)), axis=0)

    def local_solve(self, globalscheduler_variables, solver='CVXOPT'):
        mu, nu, day = globalscheduler_variables
        self.update_matrices_local_quadr_opt(day)
        fq = self.update_fq(mu, nu, day)
        x_result, f_result = solvers.with_cvxpy(self.hq, fq, self.aq, self.bq,
                                                self.aeq, self.beq, solver=solver)
        return x_result, f_result



""" Global Schedulers """


class GlobalScheduler():
    def __init__(self, data_generator, start_date, time_horizon, plot_callback=None):
        self.data_generator = data_generator
        self.start_date = start_date
        self.time_horizon = time_horizon
        self.list_localschedulers = []
        self.plot_callback = plot_callback
        self.day = 0

    def set_list_localschedulers(self, list_localschedulers):
        self.list_localschedulers = list_localschedulers

    def get_list_localschedulers(self):
        return self.list_localschedulers

    def run_global_optim(self):
        self.global_solve()

    def global_solve(self):
        raise NotImplementedError

    def get_result(self):
        raise NotImplementedError


class ModelGlobalScheduler(GlobalScheduler):
    def __init__(self):
        pass


class TravaccaEtAl2017AggGlobalScheduler(GlobalScheduler):
    def __init__(self, number_local_buildings, data_generator, start_date=32,
            time_horizon=1, plot_callback=None):
        super().__init__(data_generator, start_date, time_horizon, plot_callback=plot_callback)

        if type(self.data_generator) != datagenerators.TravaccaEtAl2017AggDataGenerator:
            raise ValueError('incorrect datagenerator type')

        self.number_local_buildings = number_local_buildings
        self.solver = 'CVXPY'
        self.alpha = 1
        self.delta = 0.01

    def get_data_generator(self):
        return self.data_generator

    def global_solver(self):
        individual_load_prediction = self.data_generator.individual_load_prediction
        pv_generation_prediction = self.data_generator.pv_generation_prediction
        prices_prediction = self.data_generator.prices_prediction
        prices_covariance_prediction = self.data_generator.prices_covariance_prediction

        grid_load_max = self.data_generator.grid_load_max
        e_min = self.data_generator.e_min
        e_max = self.data_generator.e_max
        ev_min = self.data_generator.ev_min
        ev_max = self.data_generator.ev_max
        e_max_agg = self.data_generator.e_max_agg
        e_min_agg = self.data_generator.e_min_agg
        ev_min_agg = self.data_generator.ev_min_agg
        ev_max_agg = self.data_generator.ev_max_agg

        matrix_a = np.tril(np.ones((HOURS_PER_DAY, HOURS_PER_DAY)))

        grid_load = cvxpy.Variable(self.number_local_buildings,
                self.time_horizon * HOURS_PER_DAY)
        ev_load = cvxpy.Variable(self.number_local_buildings,
                self.time_horizon * HOURS_PER_DAY)


        cost_function = cvxpy.Minimize(cvxpy.sum_entries(grid_load, axis=0) * prices_prediction
                + self.alpha * cvxpy.quad_form(cvxpy.sum_entries(grid_load, axis=0).T,
                    prices_covariance_prediction))
        + self.delta / 2 * (cvxpy.square(cvxpy.pos(cvxpy.norm(ev_load, 'fro')))
        + cvxpy.square(cvxpy.pos(cvxpy.norm(grid_load, 'fro'))))



        constraints = [individual_load_prediction + ev_load <= pv_generation_prediction + grid_load]

        constraints += [- grid_load_max <= grid_load,
                grid_load <= grid_load_max]

        epsilon = 3


        for i in range(self.number_local_buildings):
            #constraints += [e_min[i, :].T - epsilon <= matrix_a * ev_load[i, :].T,
            #        matrix_a * ev_load[i, :].T <= e_max[i, :].T + epsilon]
            constraints += [ev_min[i, :].T - epsilon <= ev_load[i, :].T,
                    ev_load[i, :].T <= ev_max[i, :].T + epsilon]

        constraints += [e_min_agg.T <= matrix_a * cvxpy.sum_entries(ev_load, axis=0).T ,
                matrix_a * cvxpy.sum_entries(ev_load, axis=0).T <= e_max_agg.T]
        constraints += [ev_min_agg.T <= cvxpy.sum_entries(ev_load, axis=0).T ,
                cvxpy.sum_entries(ev_load, axis=0).T <= ev_max_agg.T]

        prob = cvxpy.Problem(cost_function, constraints)
        prob.solve()
        self.grid_load_result = grid_load.value
        self.ev_load_result = ev_load.value
        self.final_cost = prob.value
        print('solved')
        print("status:", prob.status)
        print("optimal value", prob.value)
        #print("optimal var", grid_load.value, ev_load.value)


    def set_parameters(self, alpha=1, delta=1):
        self.alpha = alpha
        self.delta = delta

    def get_result(self):
        return (self.grid_load_result, self.ev_load_result)


class TravaccaEtAl2017GlobalScheduler(GlobalScheduler):
    def __init__(self, data_generator, start_day=32, time_horizon=1,
                 plot_callback=None):
        super().__init__(data_generator, start_day,
                time_horizon, plot_callback=plot_callback)

        if type(self.data_generator) != datagenerators.TravaccaEtAl2017DataGenerator:
            raise ValueError('incorrect datagenerator type')

        self.c = self.create_c()
        self.b = self.create_b()
        self.solver = 'CVXOPT'

    def set_solver(self, solver):
        self.solver = solver

    def get_data_generator(self):
        return self.data_generator

    def create_c(self):
        return np.reshape(np.concatenate(
            [
                self.data_generator.e_min_agg, -self.data_generator.e_max_agg,
                self.data_generator.ev_min_agg, -self.data_generator.ev_max_agg
            ],
            axis=0).T, (-1, 1))

    def create_b(self):
        a = np.tril(np.ones((HOURS_PER_DAY, HOURS_PER_DAY)))
        return np.concatenate(
            (-a.T, a.T, -np.eye(HOURS_PER_DAY), np.eye(HOURS_PER_DAY)), axis=1)

    def global_solve(self, num_iter=10, gamma=0.00001, alpha=1):
        mu, nu, g_result, ev_result, local_optimum_cost, total_cost = self.initialize_gradient_ascent(
            num_iter)
        i = 0
        delta_total_cost = 100
        previous_total_cost = 0
        while self.convergence_criteria(i, num_iter, delta_total_cost) is False:
            print('global_solve')
            g_result, ev_result, local_optimum_cost = self.next_step_gradient_ascent(
                mu, nu, g_result, ev_result, local_optimum_cost)
            total_cost[i] = self.compute_total_cost(mu, nu, alpha,
                                                    local_optimum_cost)
            mu = self.update_mu(mu, gamma, ev_result)
            nu = self.update_nu(nu, gamma, alpha, g_result)
            delta_total_cost = total_cost[i] - previous_total_cost
            i += 1
        print(self.status)
        self.plot_results(g_result, ev_result, total_cost)

    def convergence_criteria(self, i, num_iter, delta_total_cost):
        if delta_total_cost <= 30:
            self.status = 'converged'
            return True
        if i == num_iter:
            self.status = 'max iteration reached'
            return True
        return False

    def plot_results(self, g_result, ev_result, total_cost):
        if self.plot_callback is not None:
            self.plot_callback(
                    [np.sum(g_result, axis=1),
                        np.sum(ev_result, axis=1)],
                    'final load from grid and ev consumption',
                    ['g_result', 'ev_result'])
            self.plot_callback([total_cost], 'total_cost_predicted',
                    ['total cost'])
            self.plot_callback(
                    [self.data_generator.dam_price, self.data_generator.dam_demand],
                    'DAM prices and energy demand', ['dam_price', 'dam_demand'])
            self.plot_callback([
                self.data_generator.dam_predict_price,
                self.data_generator.dam_price
                ], 'DAM prices predicted and real', ['dam_predict_price', 'dam_price'])

    def update_mu(self, mu, gamma, ev_result):
        return np.maximum(mu + gamma * self.c + gamma * np.dot(
            self.b.T, np.reshape(np.sum(ev_result, axis=1), (-1, 1))),
                          np.zeros((4 * HOURS_PER_DAY, 1)))

    def update_nu(self, nu, gamma, alpha, g_result):
        return nu - gamma * 1 / (2 * alpha) * np.dot(
            np.linalg.inv(self.data_generator.cov_dam_price),
            nu) - gamma * np.reshape(np.sum(g_result, axis=1).T, (-1, 1))

    def compute_total_cost(self, mu, nu, alpha, local_optimum_cost):
        return -1 / (4 * alpha) * np.dot(
            nu.T, np.dot(np.linalg.inv(self.data_generator.cov_dam_price), nu
                         )) + np.dot(self.c.T, mu) + np.sum(local_optimum_cost)

    def initialize_gradient_ascent(self, num_iter):
        size = len(self.list_localschedulers)
        return np.zeros((HOURS_PER_DAY * 4, 1)), np.zeros(
            (HOURS_PER_DAY, 1)), np.zeros((HOURS_PER_DAY, size)), np.zeros(
                (HOURS_PER_DAY, size)), np.zeros((size, 1)), np.zeros(
                    (num_iter, 1))

    def next_step_gradient_ascent(self, mu, nu, g_result, ev_result,
            local_optimum_cost):
        globalscheduler_variables = (mu, nu, self.day)
        for i, localscheduler in enumerate(self.list_localschedulers):
            x_result, f_result = localscheduler.run_local_optim(
                    globalscheduler_variables, solver=self.solver)
            g_result[:, i] = x_result[:HOURS_PER_DAY]
            ev_result[:, i] = x_result[HOURS_PER_DAY:]
            local_optimum_cost[i, 0] = f_result
        return g_result, ev_result, local_optimum_cost
