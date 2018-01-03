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
        self.localcontroller = controllers.TravaccaEtAl2017LocalController(self.house, self.globalcontroller)

    def test_generate_random_pv_gen(self):
        self.assertEqual(self.localcontroller.generate_random_pv_gen().shape, (24,))

    def test_generate_random_load(self):
        self.assertEqual(self.localcontroller.generate_random_load().shape, (24,))

    def test_create_new_aq(self):
        self.assertEqual(self.localcontroller.create_new_aq().shape, (168, 48))

    def test_create_bq(self):
        self.assertEqual(self.localcontroller.create_bq().shape, (72,))

    def test_create_new_bq(self):
        self.assertEqual(self.localcontroller.create_new_bq().shape, (168,))

    def test_load_ev(self):
        self.assertEqual(self.localcontroller.load_e_max().shape, (24,))
        self.assertEqual(self.localcontroller.load_e_min().shape, (24,))
        self.assertEqual(self.localcontroller.load_ev_max().shape, (24,))
        self.assertEqual(self.localcontroller.load_ev_min().shape, (24,))

    def test_load_matrix_for_optim(self):
        self.assertEqual(self.localcontroller.load_b().shape, (24, 96))
        self.assertEqual(self.localcontroller.load_aeq().shape, (48,))
        self.assertEqual(self.localcontroller.load_aq().shape, (72, 48))
        self.assertEqual(self.localcontroller.load_beq().shape, ())
        self.assertEqual(self.localcontroller.load_hq().shape, (48, 48))
        self.assertEqual(self.localcontroller.load_lbq().shape, (48,))
        self.assertEqual(self.localcontroller.load_ubq().shape, (48,))


class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass


class TestLoadDataTravaccaEtAl2017GlobalController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_load_dam_price(self):
        self.assertEqual(self.globalcontroller.load_dam_price().shape, (24,))

    def test_load_cov_dam_price(self):
        self.assertEqual(self.globalcontroller.load_cov_dam_price().shape, (24, 24))

    def test_predict_price(self):
        self.assertEqual(self.globalcontroller.predict_dam_price().shape, (24, 1))


class TestRunGradientAccentTravaccaEtAl2017GlobaController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_compute_total_cost(self):
        mu = np.zeros((96, 1))
        nu = np.zeros((24, 1))
        alpha = 1
        local_optimum_cost = np.ones((50, 1))
        self.assertEqual(self.globalcontroller.compute_total_cost(mu, nu, alpha, local_optimum_cost).shape, (1, 1))


if __name__ == '__main__':
    unittest.main()
