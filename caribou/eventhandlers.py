""" event-handlers run the simulation and coordinate the different agents """

HOURS_PER_DAY = 24

class EventHandler:
    def __init__(self, time_horizon):
        self.simulation_time = time_horizon * HOURS_PER_DAY

    def run_simulation(self):
        raise NotImplementedError


class ModelEventHandler(EvenHandler):
    def __init__(self):
        super().__init__(self)
        self.storare = agents.Storage()

    def run_simulation(self):
        for i in range(self.simulation_horizon):
            unchanged_consumption = self.load_demand[i] + self.ev_demand[i] - self.pv_generation[i]
            price_to_sell = self.prices_to_sell[i]
            price_to_buy = self.prices_to_buy[i]

            if unchanged_consumption > 0:
                if self.flywheel.is_empty() or price_to_buy <= self.ref_price_to_buy:
                    self.load_from_grid[i] += unchanged_consumption
                else :
                    self.flywheel.discharge(unchanged_consumption, i)
            if unchanged_consumption < 0:
                if self.flywheel.is_full() or price_to_sell >= self.ref_price_to_sell:
                    self.load_to_grid[i] += - unchanged_consumption
                else:
                    self.flywheel.charge(- unchanged_consumption, i)
        self.total_cost = - sum(self.load_to_grid)*0.07 + np.dot(self.load_from_grid.T, self.prices_to_buy)

    def load_data(self):
        self.load_demand = get_data.import_load_demand(self.sim_number, self.sim_id)
        self.ev_demand = get_data.import_ev_demand(self.sim_number, self.sim_id)
        self.pv_generation = get_data.import_pv_generation(self.sim_number, self.sim_id)
        self.prices_to_sell = get_data.import_prices_to_sell(self.simulation_horizon)
        self.prices_to_buy = get_data.import_prices_to_buy(self.simulation_horizon)

    def plot_results(self):
        dates = [self.start_date + 3600*i for i in range(self.simulation_horizon)]
        labels = [time.strftime('%H:%M:%S', time.gmtime(date)) for date in dates]
        to_plot = [(self.load_from_grid, 'load from grid'),
            (self.load_to_grid, 'load to grid'),
            (self.flywheel.soc_record, 'flywheel load'),
            (self.load_demand, 'load demand'),
            (self.ev_demand, 'ev demand'),
            (self.pv_generation, 'pv generation'),
            ([1000*price for price in self.prices_to_buy], 'prices to buy')]
        plt.figure(figsize=(20, 10))
        for i in range(len(to_plot)):
            plt.plot(dates, to_plot[i][0], label=to_plot[i][1])
            plt.xticks(dates, labels, rotation='vertical')
            plt.tick_params(labelsize=6)
            plt.xlabel('time')
        plt.grid()
        plt.legend()
        plt.savefig('result.png')

    def get_cost(self):
        return self.total_cost


