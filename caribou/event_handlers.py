""" event-handlers for pausing processes """

import time


class EventHandler:
    def __init__(self):
        pass

    def pause_until(self, condition):
        wait_time = 0
        while not condition:
            time.sleep(1)
            wait_time += 1
        print('Wait time: ', wait_time)
