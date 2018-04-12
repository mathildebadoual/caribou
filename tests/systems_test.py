import caribou.systems as systems
import numpy as np
import unittest

""" System Tests """

HOURS_PER_DAY = 24

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.system = systems.System()
        self.y_objective = np.ones((HOURS_PER_DAY))
        self.system.set_y_objective(self.y_objective)

    def test_run_simulation(self):
        self.system.run_simulation()
        self.assertEqual(self.system.timer, 3600)
        self.assertEqual(self.system.optimization_status, 'optimal')
