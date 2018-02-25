import caribou.agents as agents
import caribou.eventhandlers as eventhandlers
import caribou.time as time
import caribou.controllers as controllers
import caribou.agentgroups as agentgroups
import unittest



class TestConstructionEV(unittest.TestCase):
    def setUp(self):
        timer = time.Timer()
        eventhandler = eventhandlers.EventHandler()
        agentgroup = agentgroups.AgentGroup(0)
        localcontroller = controllers.LocalController(timer, agentgroup, eventhandler)
        self.agent_EV = agents.EV(0, localcontroller)
        agentgroup.add(self.agent_EV)

    def test_set_state(self):
        self.agent_EV.set_status_control('charging')
        self.assertEqual(self.agent_EV.status_control, 'charging')
        self.agent_EV.set_status_current('not charging')
        self.assertEqual(self.agent_EV.status_current, 'not charging')

    def test_build_state_machine(self):
        self.assertEqual(len(self.agent_EV.transition_dict[self.agent_EV.charge]), 2)
        self.assertEqual(len(self.agent_EV.transition_dict[self.agent_EV.charge][0]), 2)


class TestConstructionBattery(unittest.TestCase):
    def setUp(self):
        timer = time.Timer()
        eventhandler = eventhandlers.EventHandler()
        agentgroup = agentgroups.AgentGroup(0)
        localcontroller = controllers.LocalController(timer, agentgroup, eventhandler)
        self.agent_B = agents.Battery(0, localcontroller)
        agentgroup.add(self.agent_B)

    def test_state(self):
        self.agent_B.set_status_control('charging')
        self.assertEqual(self.agent_B.status_control, 'charging')
        self.agent_B.set_status_current('not charging')
        self.assertEqual(self.agent_B.status_current, 'not charging')

    def test_build_state_machine(self):
        self.assertEqual(len(self.agent_B.transition_dict[self.agent_B.charge]), 1)
        self.assertEqual(len(self.agent_B.transition_dict[self.agent_B.charge][0]), 2)


class TestRunEV(unittest.TestCase):
    def setUp(self):
        timer = time.Timer()
        eventhandler = eventhandlers.EventHandler()
        agentgroup = agentgroups.AgentGroup(0)
        localcontroller = controllers.LocalController(timer, agentgroup, eventhandler)
        self.agent_EV = agents.EV(0, localcontroller)
        agentgroup.add(self.agent_EV)

    def test_run_sim(self):
        pass

if __name__ == '__main__':
    unittest.main()
