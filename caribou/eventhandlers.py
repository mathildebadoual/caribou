class EventHandler:
    def __init__(self, agent):
        self.agent = agent
        self.current_time_step = 0

    def run_next_step(self):
        self.run_step()
        self.current_time_step += 1

    def run_step(self):
        raise NotImplementedError


class EVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)


class PVevent(EventHandler):
    def __init__(self, agent):
        super().__init__(agent)
        self.irradiance_data = []

    def set_irradiance_data(self, irradiance_data):
        self.irradiance_data = irradiance_data

    def get_irradiance_data(self):
        return self.irradiance_data

    def get_instant_power_gen(self, time_step):
        self.agent.compute_instant_power_gen(
            self.irradiance_data[time_step])
        return self.agent.get_instant_power_gen()

    def run_step(self):
        try:
            irradiance_at_step_time = self.irradiance_data[
                self.current_time_step]
            self.agent.compute_instant_power_gen(irradiance_at_step_time)
            self.agent.update_accum_power_gen()
        except IndexError:
            pass
