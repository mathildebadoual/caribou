import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import caribou.agents as agents
import caribou.eventhandlers as eventhandlers
import caribou.timer as timer
import unittest


class TestConstructionLocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.globalcontroller = controllers.GlobalController(self.timer)
        self.house_controller = controllers.LocalController(
            self.house, self.globalcontroller)


class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass


class TestContrucitonTravaccaEtAl2017GlobalController(unittest.TestCase):
    def setUp(self):
        self.globalcontroller = controllers.TravaccaEtAl2017GlobalController()

    def test_data_loading(self):
        self.assertEqual(self.globalcontroller.b.shape, (24, 96))
        self.assertEqual(self.globalcontroller.data_main.shape, (37244, 17))
        self.assertEqual(self.globalcontroller.dam_price.shape, (24,))


if __name__ == '__main__':
    unittest.main()
