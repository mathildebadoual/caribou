import numpy as np
import random
import caribou.agents as agents
import caribou.agentgroups as agentgroups
import caribou.eventhandlers as eventhandlers
import caribou.controllers as controllers
import time

list_houses = []
list_localcontrollers = []

globalcontroller = controllers.TravaccaEtAl2017GlobalController(start_day=32)


for i in range(100):
    group_id = i
    house = agentgroups.ResidentialBuilding(group_id)
    list_houses.append(house)
    house.add(agents.EV(i))
    house.add(agents.PV(2 * i))

    localcontroller = controllers.TravaccaEtAl2017LocalController(house, globalcontroller)
    list_localcontrollers.append(localcontroller)

globalcontroller.set_list_localcontrollers(list_localcontrollers)

globalcontroller.run_global_optim()
