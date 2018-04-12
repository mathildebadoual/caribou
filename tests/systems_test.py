import caribou.systems as systems
import caribou.visualization as visualization
import caribou.datagenerators as datagenerators
import numpy as np
import unittest

""" System Tests """

HOURS_PER_DAY = 24

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.visual = visualization.Visualize()
        self.data_generator = datagenerators.ModelDataGenerator()
        self.system = systems.System(self.data_generator, plot_callback=self.visual)
        self.y_objective = np.array([
            [ 41.63573333, 31.36836667, 26.93901667, 28.06701667, 35.33375, 30.23021667, 24.64818333, 31.33445, 22.29681893, 9.16568038, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31.90643768, 53.57386667, 76.35911667, 58.3072    ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16.23529764, 57.76880902 , 29.74086964, 65.88500149, 65.70401239, 0, 24.54686118, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -51.4226, 0, -40.53, -32.47, -53.15, -30.2, 0, 0, 0]])
        self.system.set_y_objective(self.y_objective)

    def test_optimization(self):
        self.system.next_step()
        self.assertEqual(self.system.timer, 3600)
        self.assertEqual(self.system.optimization_status, 'optimal')

    def test_run_simulation(self):
        self.system.run_simulation()
        self.assertEqual(self.system.timer, 86400)

    def test_plot_result(self):
        self.system.run_simulation()
        self.system.plot_results()
        self.visual.plot_all()
