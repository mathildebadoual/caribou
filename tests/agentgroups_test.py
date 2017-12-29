import caribou.agentgroups as agentgroups
import caribou.agents as agents
import caribou.eventhandlers as eventhandlers
import unittest


class TestContruction(unittest.TestCase):

    def setUp(self):
        self.house = agentgroups.ResidentialBuilding(group_id=0)

    def test_house_setget_agents(self):
        EV_agent = agents.EV(agent_id=0)
        PV_agent = agents.PV(agent_id=1)
        self.house.add(EV_agent)
        self.house.add(PV_agent)
        list_agents_house = [EV_agent, PV_agent]
        self.assertEqual(self.house.get_agents(), list_agents_house)

    def test_house_list_eventhandlers(self):
        EV_agent = agents.EV(agent_id=0)
        PV_agent = agents.PV(agent_id=1)
        self.house.add(EV_agent)
        self.house.add(PV_agent)
        self.assertIsInstance(self.house.list_eventhandlers[0], eventhandlers.EventHandler)

    def test_get_instant_power_load_in_kw(self):
        for i in range(10):
            self.house.add(agents.EV(i))
            self.house.add(agents.PV(2*i))
        for i, EV_agent in enumerate(self.house.get_agents(agents.EV)):
            EV_agent.set_instant_power_load_in_kw(3)
        self.assertEqual(self.house.get_instant_net_load_in_kw(), 30)

    def test_get_acum_net_load_in_kwh(self):
        for i in range(10):
            self.house.add(agents.EV(i))
            self.house.add(agents.PV(2*i))
        for agent in self.house.get_agents():
            agent.set_instant_power_load_in_kw(1)
            agent.set_instant_power_load_in_kw(1)
        self.assertEqual(self.house.get_accum_net_load_in_kwh(), 40)



if __name__ == '__main__':
    unittest.main()
