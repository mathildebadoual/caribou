import caribou.eventhandlers as eventhandlers
import caribou.agents as agents
import caribou.agentgroups as agentgroups
import unittest

class TestConstructionEVevent(unittest.TestCase):
    def setUp(self):
        self.agent_EV = agents.EV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_EV)

    def test_init_event(self):
        self.assertIsInstance(self.house.get_list_eventhandlers()[0], eventhandlers.EVevent)

class TestConstructionPVevent(unittest.TestCase):
    def setUp(self):
        self.agent_PV = agents.PV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_PV)
        self.event = self.house.get_list_eventhandlers()[0]

    def test_init_event(self):
        self.assertIsInstance(self.house.get_list_eventhandlers()[0], eventhandlers.PVevent)

    def test_get_irradiance_data(self):
        irradiance_data = [0.1, 0.2, 0.3]
        self.event.set_irradiance_data(irradiance_data)
        self.assertEqual(self.event.get_irradiance_data(), irradiance_data)

class TestRunAgentPV(unittest.TestCase):
    def setUp(self):
        self.agent_PV = agents.PV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_PV)
        self.event_PV = self.house.get_list_eventhandlers()[0]
        self.irradiance_data = [0.1, 0.2, 0.3]
        self.event_PV.set_irradiance_data(self.irradiance_data)

    def test_get_instant_power_gen(self):
        self.agent_PV.set_angle(90)
        self.agent_PV.set_efficiency(0.5)
        time_step = 0
        self.assertEqual(self.event_PV.get_instant_power_gen(time_step), 90*0.5*self.irradiance_data[time_step])

    def test_run_step(self):
        self.agent_PV.set_angle(90)
        self.agent_PV.set_efficiency(0.5)
        for i in range(4):
            self.event_PV.run_next_step()
        self.assertEqual(self.agent_PV.get_accum_power_gen(), sum([90*0.5*ir for ir in self.irradiance_data]))

if __name__ == '__main__':
    unittest.main()
