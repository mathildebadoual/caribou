
class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.power_load = 0
        self.power_gen = 0
        self.accum_power_load = 0  # accumulated power load in kWH
        self.accum_power_gen = 0  # accumulated power generation in kWH

    def get_id(self):
        return self.agent_id

    def get_instant_power_gen(self):
        return self.power_gen

    def get_instant_power_load(self):
        return self.power_load

    def set_instant_power_load(self, power_load):
        self.power_load = power_load

    def update_accum_power_load(self):
        self.accum_power_load += self.power_load

    def set_instant_power_gen(self, power_gen):
        self.power_gen = power_gen

    def update_accum_power_gen(self):
        self.accum_power_gen += self.power_gen

    def get_accum_power_load(self):
        return self.accum_power_load

    def get_accum_power_gen(self):
        return self.accum_power_gen

class PV(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)


class EV(Agent):
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.status = 'charging'
        self.graph_status = {
                'charging': ['discharging', 'nothing'],
                'discharging': ['charging', 'nothing'],
                'nothing': ['charging', 'nothing']}

    def get_status(self):
        return self.status

# TODO: ADD ENERGY COMPONENTS (e.g., ESS, HVAC)
