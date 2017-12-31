import unittest
import random
import caribou.agents as agents
import caribou.agentgroups as agentgroups
import caribou.eventhandlers as eventhandlers

class TestContructionHouse(unittest.TestCase):

    def setUp(self):
        self.house1 = agentgroups.ResidentialBuilding(group_id=0)
        self.EV_0 = agents.EV(id=0)
        self.EV_1 = agents.EV(_id=1)
        self.PV_0 = agents.PV(_id=0)
        self.house1.add(self.EV_0)
        self.house1.add(self.EV_1)
        self.house1.add(self.PV_0)

    def test_house_get_agents_type(self):
        list_agents_house1_EV = [self.EV_0, self.EV_1]
        self.assertEqual(self.house1.get_agents(agents.EV), list_agents_house1_EV)


class TestContructionAgent(unittest.TestCase):

    def setUp(self):

        self.group_id = 1
        self.house = agentgroups.ResidentialBuilding(self.group_id)
        for i in range(10):
            self.house.add(agents.EV(i))
            self.house.add(agents.PV(2*i))


    def test_get_id(self):
        EV_agent = self.house.get_agents(agents.EV)[5]
        self.assertEqual(EV_agent.get_id(), 5)

    def test_get_instant_power_load(self):
        EV_agent = self.house.get_agents(agents.EV)[0]
        EV_agent.set_instant_power_load(3)
        self.assertEqual(EV_agent.get_instant_power_load(), 3)

    def test_get_instant_net_load(self):
        for i, EV_agent in enumerate(self.house.get_agents(agents.EV)):
            EV_agent.set_instant_power_load(3)
        self.assertEqual(self.house.get_instant_net_load(), 30)

    def test_get_instant_power_gen(self):
        PV_agent = self.house.get_agents(agents.PV)[0]
        PV_agent.set_instant_power_gen(4)
        self.assertEqual(PV_agent.get_instant_power_gen(), 4)

    def test_get_instant_net_gen(self):
        for i, PV_agent in enumerate(self.house.get_agents(agents.PV)):
            PV_agent.set_instant_power_gen(4)
        self.assertEqual(self.house.get_instant_net_gen(), 40)

    def test_update_accum_power_load(self):
        EV_agent = self.house.get_agents(agents.EV)[0]
        EV_agent.set_instant_power_load(10)
        EV_agent.update_accum_power_load(1)
        self.assertEqual(EV_agent.get_)


class TestUpdatePower(unittest.TestCase):

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
