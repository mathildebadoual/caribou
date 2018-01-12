import caribou.events as events
import caribou.agents as agents
import caribou.agentgroups as agentgroups
import unittest

class TestConstructionEVevent(unittest.TestCase):
    def setUp(self):
        self.agent_EV = agents.EV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_EV)

    def test_init_event(self):
        self.assertIsInstance(self.house.get_list_events()[0], events.EVevent)

class TestConstructionPVevent(unittest.TestCase):
    def setUp(self):
        self.agent_PV = agents.PV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_PV)
        self.event = self.house.get_list_events()[0]

    def test_init_event(self):
        self.assertIsInstance(self.house.get_list_events()[0], events.PVevent)


class TestRunAgentPV(unittest.TestCase):
    def setUp(self):
        self.agent_PV = agents.PV(agent_id=0)
        self.house = agentgroups.ResidentialBuilding(group_id=0)
        self.house.add(self.agent_PV)
        self.event_PV = self.house.get_list_events()[0]

if __name__ == '__main__':
    unittest.main()
