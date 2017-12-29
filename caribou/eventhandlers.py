class EventHandler:
    def __init__(self, agent):
        self.agent = agent


class EVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)

class PVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)
        self.irradiance_data = []
        self.current_time_step = 0

    def set_irradiance_data(self, irradiance_data):
        self.irradiance_data = irradiance_data

    def get_irradiance_data(self):
        return self.irradiance_data

    def get_instant_power_gen_in_kw(self, time_step):
        self.agent.compute_instant_power_gen_in_kw(self.irradiance_data[time_step])
        return self.agent.get_instant_power_gen_in_kw()

    def run_next_step(self):
        try:
            irradiance_at_step_time = self.irradiance_data[self.current_time_step]
            self.agent.compute_instant_power_gen_in_kw(irradiance_at_step_time)
            self.agent.update_accum_power_gen_in_kw()
            self.current_time_step += 1
        except IndexError:
            pass

