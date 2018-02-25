""" Agent Groups """



class AgentGroup:
    def __init__(self, group_id):
        self.group_id = group_id
        self.agents_list = []
        self.local_controller = None

    def add(self, agent):
        self.agents_list.append(agent)

    def remove(self, agent):
        self.agents_list.remove(agent)

    def get_group_id(self):
        return self.group_id

    def get_agents(self, agent_type=None):
        if agent_type:
            return [agent for agent in self.agents_list if isinstance(agent, agent_type)]
        return self.agents_list
