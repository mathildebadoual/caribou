import numpy as np
import caribou.agents as agents
import caribou.schedulers as schedulers
import caribou.visualization as visualization
import caribou.agentgroups as agentgroups

visualize = visualization.Visualize()

np.random.seed(seed=1)

list_houses = []
list_localschedulers = []
globalscheduler = schedulers.TravaccaEtAl2017GlobalScheduler(
        start_day=32, plot_callback=visualize.callback)
data_generator = globalscheduler.get_data_generator()

for i in range(50):
    group_id = i
    house = agentgroups.AgentGroup(group_id)
    list_houses.append(house)
    house.add(agents.EV(i))
    house.add(agents.PV(2 * i))

    localscheduler = schedulers.TravaccaEtAl2017LocalScheduler(
            house, globalscheduler, data_generator, plot_callback=visualize.callback)
    list_localschedulers.append(localscheduler)

globalscheduler.set_list_localschedulers(list_localschedulers)

globalscheduler.run_global_optim()

visualize.plot_all()




