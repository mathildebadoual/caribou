import caribou.eventhandlers as eventhandlers

class Controller:
    def __init__(self):
        pass


class LocalController(Controller):

    def __init__(self, agent_group, global_controller, list_event_handlers):
        super().__init__()
        self.agentgroup = agent_group
        self.global_controller = global_controller
        self.timer = global_controller.get_timer()
        # self.EV_charging_event = eventhandlers.EVCharging()
        # self.EV_discharging_event = eventhandlers.EVDischarging()
        # self.EV_driving_event = eventhandlers.EVDriving()
        # self.PV_generating_event = eventhandlers.PVGenerating()



class GlobalController(Controller):

    def __init__(self, timer):
        super().__init__()
        self.list_local_controllers = []
        self.timer = timer

    def set_list_local_controllers(self, list_local_controllers):
        self.list_local_controllers = list_local_controllers

    def get_list_local_controllers(self):
        return self.list_local_controllers

    def update_time_step(self, time_delta_s=3600):
        self.timer.set_next_time_step(time_delta_s)

    def get_timer(self):
        return self.timer






