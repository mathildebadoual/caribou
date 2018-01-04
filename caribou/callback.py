import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class CallBackPlot():
    def __init__(self):
        self.plot_waiting = []

    def plot(self, to_plot, title):
        plt.figure(figsize=(10, 5))
        for element in to_plot:
            plt.plot(element)
        plt.title(title)
        plt.show()

    def add(self, to_plot, title):
        self.plot_waiting.append((to_plot, title))

    def plot_all(self):
        for group_plot in self.plot_waiting:
            self.plot(group_plot[0], group_plot[1])
