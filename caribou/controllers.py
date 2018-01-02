import numpy as np
"""Controllers."""


class Controller:
    def __init__(self):
        pass


class LocalController(Controller):
    def __init__(self, agentgroup, globalcontroller):
        super().__init__()
        self.agentgroup = agentgroup
        self.globalcontroller = globalcontroller

    def run_local_optim(self, globalcontroller_variables):
        x_result, f_result = self.local_solve(globalcontroller_variables)
        return x_result, f_result

    def local_solve(self, globalcontroller_variables):
        raise NotImplementedError


class TravaccaEtAl2017LocalController(LocalController):
    def __init__(self, agentgroup, globalcontroller):
        super().__init__(agentgroup, globalcontroller)

    def local_solve(self, globalcontroller_variables):
        mu, nu, fq = globalcontroller_variables


class GlobalController(Controller):
    def __init__(self):
        super().__init__()
        self.list_localcontrollers = []

    def set_list_localcontrollers(self, list_localcontrollers):
        self.list_localcontrollers = list_localcontrollers

    def get_list_localcontrollers(self):
        return self.list_localcontrollers

    def run_global_optim(self):
        self.global_solve()

    def global_solve(self):
        raise NotImplementedError


class TravaccaEtAl2017GlobalController(GlobalController):
    def __init__(self, num_iter=50, start_day=2, time_horizon=24):
        super().__init__()
        self.num_iter = num_iter
        self.b = np.genfromtxt('data/travacca_et_al_2017/b.csv', delimiter=',')
        self.data_main = np.genfromtxt(
            'data/travacca_et_al_2017/main.csv', delimiter=',')
        self.dam_price = self.select_dam_price(start_day, time_horizon)

    def select_dam_price(self, start_day, time_horizon):
        start = start_day*4*24+1
        stop = start_day*4*24+time_horizon*4
        scale_price = 1000
        return self.data_main[start:stop:4, 11]/scale_price

    def global_solve(self):
        pass
        # mu = 0
        # nu = 0
        # ev_sol = np.zeros((24, len(self.list_localcontrollers)))
        # g_sol = np.zeros((24, len(self.list_localcontrollers)))
        # local_optimal_cost = np.zeros((len(self.list_localcontrollers), 1))
        # for _ in range(self.num_iter):
        #    fq = np.array(c.dam_predict - nu, np.dot(self.b, mu))
        #    globalcontroller_variables = (mu, nu, fq)
        #    for localcontroller in self.list_localcontrollers:
        #        localcontroller.run_local_optim(globalcontroller_variables)
