import caribou.controllers as controllers
import caribou.agents as agents
import caribou.eventhandlers as eventhandlers

class AgentGroup:

    def __init__(self, group_id):
        self.group_id = group_id
        self.agents_list = []
        self.local_controller = None
        self.list_eventhandlers = []

    def add(self, agent):
        agent.set_group_id(self.group_id)
        self.agents_list.append(agent)
        if isinstance(agent, agents.EV):
            self.list_eventhandlers.append(eventhandlers.EVevent(agent))

    def remove(self, agent):
        self.agents_list.remove(agent)

    def get_group_id(self):
        return self.group_id

    def get_agents(self, agent_type=None):
        if agent_type:
            return [agent for agent in self.agents_list if isinstance(agent, agent_type)]
        return self.agents_list

    # TODO: add functions to collect instances of specific energy components

    def get_instant_net_load_in_kw(self):
        loads = (agent.get_instant_power_load_in_kw() for agent in self.agents_list)
        return sum(loads)

    def get_instant_net_gen_in_kw(self):
        gens = (agent.get_instant_power_gen_in_kw() for agent in self.agents_list)
        return sum(gens)

    def get_accum_net_load_in_kwh(self):  # TODO: replace the list summation with looping over generator
        return np.sum([agent.get_accum_power_load_in_kwh() for agent in self.agents_list])

    def get_accum_net_gen_in_kwh(self):  # TODO: replace the list summation with looping over generator
        return np.sum([agent.get_accum_power_gen_in_kwh() for agent in self.agents_list])

    def set_local_comtroller(self, local_controller):
        self.local_controller = local_controller





class ResidentialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)


class CommercialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)

# TODO: ADD OTHER DISTINGUISHED AGENT GROUPS (e.g., University)
