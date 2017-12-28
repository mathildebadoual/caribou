class Time():

    def __init__(self, start_time_s=0, end_time_s=86400):
        self.start_time_s = start_time_s
        self.end_time_s = end_time_s
        self.time_s = start_time_s

    def set_next_time_step(self, time_delta_s=3600):
        self.time_s += time_delta_s

    def get_time(self, type='s'):

        if type == 's':
            return self.time_s

        m = self.time_s/60
        if type == 'm':
            return m

        h = self.time_s/60
        if type == 'h':
            return h

        m, s = divmod(self.time_s, 60)
        h, m = divmod(m, 60)
        if type == None:
            return h, m, s




