import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import caribou.agents as agents
import caribou.eventhandlers as eventhandlers
import caribou.timer as timer
import unittest

class TestConstructionLocalController(unittest.TestCase):
    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(0)
        self.timer = timer.Timer()
        self.globalcontroller = controllers.GlobalController(self.timer)
        self.house_controller = controllers.LocalController(self.house, self.globalcontroller)

class TestConstructionGlobalController(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
