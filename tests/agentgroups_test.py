import caribou.agentgroups as agentgroups
import caribou.agents as agents
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
        pass

if __name__ == '__main__':
    unittest.main()
