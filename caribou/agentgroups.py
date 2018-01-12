class AgentGroup:
    def __init__(self, group_id):
        self.group_id = group_id
        self.list_agents = []
        self.local_controller = None

    def add(self, agent):
        self.list_agents.append(agent)

    def remove(self, agent):
        self.list_agents.remove(agent)

    def get_group_id(self):
        return self.group_id

    def get_list_agents(self, agent_type=None):
        if agent_type:
            return [
                agent for agent in self.list_agents
                if isinstance(agent, agent_type)
            ]
        return self.list_agents

    def get_instant_net_load(self):
        loads = (agent.get_instant_power_load() for agent in self.list_agents)
        return sum(loads)

    def get_instant_net_gen(self):
        gens = (agent.get_instant_power_gen() for agent in self.list_agents)
        return sum(gens)

    def get_accum_net_load(self):  # TODO: replace the list summation with looping over generator
        return sum([agent.get_accum_power_load() for agent in self.list_agents])

    def get_accum_net_gen(self):  # TODO: replace the list summation with looping over generator
        return sum([agent.get_accum_power_gen() for agent in self.list_agents])

    def set_local_comtroller(self, local_controller):
        self.local_controller = local_controller


class ResidentialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)


class CommercialBuilding(AgentGroup):
    def __init__(self, group_id):
        super().__init__(group_id)

# TODO: ADD OTHER DISTINGUISHED AGENT GROUPS (e.g., University)
