""" Controllers of the simulation """

class GlobalController:
    def __init__(self, timer, localcontroller_list):
        self.timer = timer
        self.localcontroller_list


class LocalController:
    def __init__(self, timer, agent_group):
        self.timer = timer
        self.agent_group = agent_group

    def run_control(self):
        pass

    def check_time_max(self):
        return self.timer.time < self.timer.end_time

    def updated(self):
        # TODO(Mathilde): Put a PID controller over all the group
        return True
