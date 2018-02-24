class Timer():
    def __init__(self, start_time=0, end_time=86400):
        self.start_time = start_time
        self.end_time = end_time
        self.time = start_time

    def get_end_time(self):
        return self.end_time

    def set_next_time_step(self, time_delta=1):
        self.time += time_delta

    def get_time(self):
        return self.time
