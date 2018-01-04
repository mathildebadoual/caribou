import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import numpy as np
import unittest


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
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(
            self.house, self.globalcontroller)

    def test_generate_random_pv_gen(self):
        self.assertEqual(self.localcontroller.generate_random_pv_gen().shape,
                         (24, ))

    def test_generate_random_load(self):
        self.assertEqual(self.localcontroller.generate_random_load().shape,
                         (24, ))

    def test_create_new_aq(self):
        self.assertEqual(self.localcontroller.create_new_aq().shape, (168, 48))

    def test_create_bq(self):
        self.assertEqual(self.localcontroller.create_bq().shape, (72, 1))

    def test_create_new_bq(self):
        self.assertEqual(self.localcontroller.create_new_bq().shape, (168, 1))

    def test_load_ev(self):
        self.assertEqual(self.localcontroller.e_max.shape, (24, ))
        self.assertEqual(self.localcontroller.e_min.shape, (24, ))
        self.assertEqual(self.localcontroller.ev_max.shape, (24, ))
        self.assertEqual(self.localcontroller.ev_min.shape, (24, ))

    def test_load_matrix_for_optim(self):
        self.assertEqual(self.localcontroller.b.shape, (24, 96))
        self.assertEqual(self.localcontroller.aeq.shape, (1, 48))
        self.assertEqual(self.localcontroller.aq.shape, (72, 48))
        self.assertEqual(self.localcontroller.beq.shape, (1, 1))
        self.assertEqual(self.localcontroller.hq.shape, (48, 48))
        self.assertEqual(self.localcontroller.lbq.shape, (48, 1))
        self.assertEqual(self.localcontroller.ubq.shape, (48, 1))


class TestRunOptimTravaccaEtAl2017LocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(
            self.house, self.globalcontroller)

    def test_local_solve(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((24, 1))
        self.assertEqual(
            self.localcontroller.local_solve((mu, nu))[0].shape, (48, ))


class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass


class TestLoadDataTravaccaEtAl2017GlobalController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_loads(self):
        self.assertEqual(self.globalcontroller.dam_price.shape, (24, ))
        self.assertEqual(self.globalcontroller.dam_demand.shape, (24, ))
        self.assertEqual(self.globalcontroller.cov_dam_price.shape, (24, 24))
        self.assertEqual(self.globalcontroller.c.shape, (96, 1))
        self.assertEqual(self.globalcontroller.pv_gen.shape, (24,))

    def test_predict_price(self):
        self.assertEqual(self.globalcontroller.predict_dam_price().shape,
                         (24, 1))


class TestRunGradientAscentTravaccaEtAl2017GlobaController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()
        self.house = agentgroups.ResidentialBuilding(0)
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(
            self.house, self.globalcontroller)
        self.globalcontroller.set_list_localcontrollers([self.localcontroller])

    def test_initialize_gradient_ascent(self):
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[0].shape,
            (96, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[1].shape,
            (24, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[2].shape,
            (24, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[3].shape,
            (24, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[4].shape,
            (1, 1))
        self.assertEqual(
            self.globalcontroller.initialize_gradient_ascent(10)[5].shape,
            (10, 1))

    def test_compute_total_cost(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((24, 1))
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
        ev_result = np.zeros((24, 1))
        self.assertEqual(
            self.globalcontroller.update_mu(mu, gamma, ev_result).shape,
            (96, 1))

    def test_update_nu(self):
        nu = np.zeros((24, 1))
        gamma = 0.00001
        alpha = 1
        g_result = np.zeros((24, 1))
        self.assertEqual(
            self.globalcontroller.update_nu(nu, gamma, alpha, g_result).shape,
            (24, 1))

    def test_next_step_gradient_ascent(self):
        pass

    def test_global_solve(self):
        pass


if __name__ == '__main__':
    unittest.main()
