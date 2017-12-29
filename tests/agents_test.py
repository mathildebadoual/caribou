import caribou.agents as agents
import caribou.agentgroups as agentgroups
import unittest

class TestContructionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = agents.Agent(0)

    def test_get_id(self):
        self.assertEqual(self.agent.get_id(), 0)

    def test_get_instant_power_gen_in_kw(self):
        self.agent.set_instant_power_gen_in_kw(1)
        self.assertEqual(self.agent.get_instant_power_gen_in_kw(), 1)

    def test_get_instant_power_load_in_kw(self):
        self.agent.set_instant_power_load_in_kw(2)
        self.assertEqual(self.agent.get_instant_power_load_in_kw(), 2)

    def test_get_accum_power_load_in_kwh(self):
        for i in range(10):
            self.agent.set_instant_power_load_in_kw(1)
        self.assertEqual(self.agent.get_accum_power_load_in_kwh(), 10)


class TestConstructionEV(unittest.TestCase):
    def setUp(self):
        agent_EV = agents.EV(0)

class TestConstructionPV(unittest.TestCase):
    def setUp(self):
        agent_PV = agents.PV(0)

if __name__ == '__main__':
    unittest.main()
