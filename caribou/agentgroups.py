import caribou.agents as agents
import caribou.events as events

class AgentGroup:

    def __init__(self, group_id):
        self.group_id = group_id
        self.agents_list = []
        self.local_controller = None
        self.list_events = []

    def add(self, agent):
        self.agents_list.append(agent)
        if isinstance(agent, agents.EV):
            self.list_events.append(events.EVevent(agent))
        if isinstance(agent, agents.PV):
            self.list_events.append(events.PVevent(agent))

    def remove(self, agent):
        self.agents_list.remove(agent)

    def get_group_id(self):
        return self.group_id

    def get_agents(self, agent_type=None):
        if agent_type:
            return [agent for agent in self.agents_list if isinstance(agent, agent_type)]
        return self.agents_list

    # TODO: add functions to collect instances of specific energy components

    def get_instant_net_load(self):
        loads = (agent.get_instant_power_load() for agent in self.agents_list)
        return sum(loads)

    def get_instant_net_gen(self):
        gens = (agent.get_instant_power_gen() for agent in self.agents_list)
        return sum(gens)

    def get_accum_net_load(self):  # TODO: replace the list summation with looping over generator
        return sum([agent.get_accum_power_load() for agent in self.agents_list])

    def get_accum_net_gen(self):  # TODO: replace the list summation with looping over generator
        return sum([agent.get_accum_power_gen() for agent in self.agents_list])

    def set_local_comtroller(self, local_controller):
        self.local_controller = local_controller

    def get_list_events(self):
        return self.list_events




class ResidentialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)


class CommercialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)

# TODO: ADD OTHER DISTINGUISHED AGENT GROUPS (e.g., University)
