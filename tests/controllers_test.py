import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import numpy as np
import unittest


HOURS_PER_DAY = 24

class TestConstructionLocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.globalcontroller = controllers.GlobalController()
        self.housecontroller = controllers.LocalController(
            self.house, self.globalcontroller)


class TestLoadDataTravaccaEtAl2017LocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()
        data_generator = self.globalcontroller.get_data_generator()
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(
            self.house, self.globalcontroller, data_generator)

    def test_load_matrix_for_optim(self):
        day = 0
        self.localcontroller.update_matrices_local_quadr_opt(day)
        self.assertEqual(self.localcontroller.aeq.shape, (1, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localcontroller.aq.shape, (7 * HOURS_PER_DAY, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localcontroller.beq.shape, (1, 1))
        self.assertEqual(self.localcontroller.hq.shape, (2 * HOURS_PER_DAY, 2 * HOURS_PER_DAY))
        self.assertEqual(self.localcontroller.lbq.shape, (2 * HOURS_PER_DAY, 1))
        self.assertEqual(self.localcontroller.ubq.shape, (2 * HOURS_PER_DAY, 1))
        self.assertEqual(self.localcontroller.bq.shape, (7 * HOURS_PER_DAY, 1))

    def test_update_fq(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        day = 0
        self.localcontroller.update_matrices_local_quadr_opt(day)
        self.assertEqual(self.localcontroller.update_fq(mu, nu, day).shape, (2 * HOURS_PER_DAY, 1))


class TestRunOptimTravaccaEtAl2017LocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()
        data_generator = self.globalcontroller.get_data_generator()
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(
                self.house, self.globalcontroller, data_generator)

    def test_local_solve(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        day = 0
        self.assertEqual(
            self.localcontroller.local_solve((mu, nu, day))[0].shape, (2 * HOURS_PER_DAY,))


class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass


class TestLoadDataTravaccaEtAl2017GlobalController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_create_c(self):
        self.assertEqual(self.globalcontroller.c.shape, (4 * HOURS_PER_DAY, 1))

    def test_create_b(self):
        self.assertEqual(self.globalcontroller.b.shape, (HOURS_PER_DAY, 4 * HOURS_PER_DAY))


class TestRunGradientAscentTravaccaEtAl2017GlobaController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()
        self.data_generator = self.globalcontroller.get_data_generator()
        self.list_localcontrollers = []
        for i in range(10):
            group_id = i
            house = agentgroups.ResidentialBuilding(group_id)
            localcontroller = controllers.TravaccaEtAl2017LocalController(house, self.globalcontroller, self.data_generator)
            self.list_localcontrollers.append(localcontroller)
        self.globalcontroller.set_list_localcontrollers(self.list_localcontrollers)

    def test_initialize_gradient_ascent(self):
        size = len(self.list_localcontrollers)
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[0].shape,
            (4 * HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[1].shape,
            (HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[2].shape,
            (HOURS_PER_DAY, size))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[3].shape,
            (HOURS_PER_DAY, size))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[4].shape,
            (size, 1))

    def test_compute_total_cost(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((HOURS_PER_DAY, 1))
        alpha = 1
        local_optimum_cost = np.ones((50, 1))
        self.assertEqual(
            self.globalcontroller.compute_total_cost(
                mu, nu, alpha, local_optimum_cost).shape, (1, 1))
        self.assertEqual(
            self.globalcontroller.compute_total_cost(mu, nu, alpha,
                                                     local_optimum_cost), 50)

    def test_update_mu(self):
        mu = np.zeros((96, 1))
        gamma = 0.00001
        ev_result = np.zeros((HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalcontroller.update_mu(mu, gamma, ev_result).shape,
            (96, 1))

    def test_update_nu(self):
        nu = np.zeros((HOURS_PER_DAY, 1))
        gamma = 0.00001
        alpha = 1
        g_result = np.zeros((HOURS_PER_DAY, 1))
        self.assertEqual(
            self.globalcontroller.update_nu(nu, gamma, alpha, g_result).shape,
            (HOURS_PER_DAY, 1))

    def test_global_solve(self):
        self.globalcontroller.run_global_optim()
        self.assertEqual(self.globalcontroller.status, 'converge')


if __name__ == '__main__':
    unittest.main()
