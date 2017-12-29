import caribou.eventhandlers as eventhandlers

class Controller:
    def __init__(self):
        pass


class LocalController(Controller):

    def __init__(self, agentgroup, global_controller):
        super().__init__()
        self.agentgroup = agentgroup
        self.globalcontroller = globalcontroller
        self.timer = globalcontroller.get_timer()

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






