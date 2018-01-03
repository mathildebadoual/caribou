import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import caribou.agents as agents
import caribou.eventhandlers as eventhandlers
import caribou.timer as timer
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




class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass


class TestLoadDataTravaccaEtAl2017GlobalController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_load_b_matrix(self):
        self.assertEqual(self.globalcontroller.load_b_matrix().shape, (24, 96))

    def test_load_dam_price(self):
        self.assertEqual(self.globalcontroller.load_dam_price().shape, (24,))

    def test_load_cov_dam_price(self):
        self.assertEqual(self.globalcontroller.load_cov_dam_price().shape, (24, 24))

    def test_predict_price(self):
        self.assertEqual(self.globalcontroller.predict_dam_price().shape, (24, 1))


if __name__ == '__main__':
    unittest.main()
