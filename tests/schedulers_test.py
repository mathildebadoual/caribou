import caribou.schedulers as schedulers
import caribou.agentgroups as agentgroups
import caribou.datagenerators as datagenerators
import numpy as np
import unittest


HOURS_PER_DAY = 24


""" Local Schedulers Tests """


class TestConstructionLocalScheduler(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.AgentGroup(0)
        self.datagenerator = datagenerators.DataGenerator()
        self.globalscheduler = schedulers.GlobalScheduler()
        self.housescheduler = schedulers.LocalScheduler(
            self.house, self.globalscheduler)


class TestLoadDataTravaccaEtAl2017LocalScheduler(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.AgentGroup(0)
        self.data_generator = datagenerators.TravaccaEtAl2017DataGenerator()
        self.globalscheduler = schedulers.TravaccaEtAl2017GlobalScheduler(self.data_generator)
        data_generator = self.globalscheduler.get_data_generator()
        self.localscheduler = schedulers.TravaccaEtAl2017LocalScheduler(
            self.house, self.globalscheduler, data_generator)

    def test_load_matrix_for_optim(self):
        day = 0
        self.localscheduler.update_matrices_local_quadr_opt(day)
        self.assertEqual(self.localscheduler.aeq.shape, (1, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localscheduler.aq.shape, (7 * HOURS_PER_DAY, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localscheduler.beq.shape, (1, 1))
        self.assertEqual(self.localscheduler.hq.shape, (2 * HOURS_PER_DAY, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localscheduler.lbq.shape, (2 * HOURS_PER_DAY, 1))
        self.assertEqual(self.localscheduler.ubq.shape, (2 * HOURS_PER_DAY, 1))
        self.assertEqual(self.localscheduler.bq.shape, (7 * HOURS_PER_DAY, 1))

    def test_update_fq(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        day = 0
        self.localscheduler.update_matrices_local_quadr_opt(day)
        self.assertEqual(self.localscheduler.update_fq(mu, nu, day).shape, (2 * HOURS_PER_DAY, 1))


class TestRunOptimTravaccaEtAl2017LocalScheduler(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.AgentGroup(0)
        self.data_generator = datagenerators.TravaccaEtAl2017DataGenerator()
        self.globalscheduler = schedulers.TravaccaEtAl2017GlobalScheduler(self.data_generator)
        data_generator = self.globalscheduler.get_data_generator()
        self.localscheduler = schedulers.TravaccaEtAl2017LocalScheduler(
                self.house, self.globalscheduler, data_generator)

    def test_local_solve(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        day = 0
        self.assertEqual(
            self.localscheduler.local_solve((mu, nu, day))[0].shape, (2 * HOURS_PER_DAY,))



""" Global Scheduler Tests """

class TestConstructionGlobalScheduler(unittest.TestCase):
    def setUp(self):
        pass


class TestTravaccaEtAl2017AggGlobalScheduler(unittest.TestCase):
    def setUp(self):
        self.number_local_buildings = 10
        self.data_generator = datagenerators.TravaccaEtAl2017AggDataGenerator(self.number_local_buildings)
        self.globalscheduler = schedulers.TravaccaEtAl2017AggGlobalScheduler(self.number_local_buildings, self.data_generator)
        self.data_generator = self.globalscheduler.get_data_generator()
        self.globalscheduler.global_solver()

    def test_global_solver(self):
        self.assertAlmostEqual(self.globalscheduler.final_cost, 12, places=0)

    def test_get_result(self):
        self.assertEqual(self.globalscheduler.get_result()[1].shape, (self.number_local_buildings, HOURS_PER_DAY))


class TestLoadDataTravaccaEtAl2017GlobalScheduler(unittest.TestCase):
    def setUp(self):
        self.data_generator = datagenerators.TravaccaEtAl2017DataGenerator()
        self.globalscheduler = schedulers.TravaccaEtAl2017GlobalScheduler(self.data_generator)

    def test_create_c(self):
        self.assertEqual(self.globalscheduler.c.shape, (4 * HOURS_PER_DAY, 1))

    def test_create_b(self):
        self.assertEqual(self.globalscheduler.b.shape, (HOURS_PER_DAY, 4 * HOURS_PER_DAY))


class TestRunGradientAscentTravaccaEtAl2017GlobaScheduler(unittest.TestCase):
    def setUp(self):
        self.number_localschedulers = 10
        self.data_generator = datagenerators.TravaccaEtAl2017DataGenerator()
        self.globalscheduler = schedulers.TravaccaEtAl2017GlobalScheduler(self.data_generator)
        self.list_localschedulers = []
        for i in range(self.number_localschedulers):
            group_id = i
            house = agentgroups.AgentGroup(group_id)
            localscheduler = schedulers.TravaccaEtAl2017LocalScheduler(house, self.globalscheduler, self.data_generator)
            self.list_localschedulers.append(localscheduler)
        self.globalscheduler.set_list_localschedulers(self.list_localschedulers)

    def test_initialize_gradient_ascent(self):
        size = len(self.list_localschedulers)
        self.assertEqual(
            self.globalscheduler.initialize_gradient_ascent(10)[0].shape,
            (4 * HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalscheduler.initialize_gradient_ascent(10)[1].shape,
            (HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalscheduler.initialize_gradient_ascent(10)[2].shape,
            (HOURS_PER_DAY, size))
        self.assertEqual(
            self.globalscheduler.initialize_gradient_ascent(10)[3].shape,
            (HOURS_PER_DAY, size))
        self.assertEqual(
            self.globalscheduler.initialize_gradient_ascent(10)[4].shape,
            (size, 1))

    def test_compute_total_cost(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        alpha = 1
        local_optimum_cost = np.ones((50, 1))
        self.assertEqual(
            self.globalscheduler.compute_total_cost(
                mu, nu, alpha, local_optimum_cost).shape, (1, 1))
        self.assertEqual(
            self.globalscheduler.compute_total_cost(mu, nu, alpha,
                                                     local_optimum_cost), 50)

    def test_update_mu(self):
        mu = np.zeros((96, 1))
        gamma = 0.00001
        ev_result = np.zeros((HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalscheduler.update_mu(mu, gamma, ev_result).shape,
            (96, 1))

    def test_update_nu(self):
        nu = np.zeros((HOURS_PER_DAY, 1))
        gamma = 0.00001
        alpha = 1
        g_result = np.zeros((HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalscheduler.update_nu(nu, gamma, alpha, g_result).shape,
            (HOURS_PER_DAY, 1))

    def test_global_solve(self):
        self.globalscheduler.run_global_optim()
        self.assertEqual(self.globalscheduler.status, 'converged')


if __name__ == '__main__':
    unittest.main()
