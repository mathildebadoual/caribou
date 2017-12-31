import caribou.agents as agents
import unittest


class TestContructionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = agents.Agent(0)

    def test_get_id(self):
        self.assertEqual(self.agent.get_id(), 0)

    def test_get_instant_power_gen(self):
        self.agent.set_instant_power_gen(1)
        self.assertEqual(self.agent.get_instant_power_gen(), 1)

    def test_get_instant_power_load(self):
        self.agent.set_instant_power_load(2)
        self.assertEqual(self.agent.get_instant_power_load(), 2)

    def test_get_accum_power_load(self):
        for i in range(10):
            self.agent.set_instant_power_load(1)
            self.agent.update_accum_power_load()
        self.assertEqual(self.agent.get_accum_power_load(), 10)


class TestConstructionEV(unittest.TestCase):
    def setUp(self):
        self.agent_EV = agents.EV(0)

    def test_get_status(self):
        self.agent_EV.set_status('Charging')
        self.assertEqual(self.agent_EV.get_status(), 2)


class TestConstructionPV(unittest.TestCase):
    def setUp(self):
        self.agent_PV = agents.PV(0)


if __name__ == '__main__':
    unittest.main()
