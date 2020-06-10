# Peter Stephensen, DREAM 2019
import sys, os
sys.path.append(os.getcwd()) # Add root-dir to sys.path

from dream_agent import Agent
import random, matplotlib.pyplot as plt
#----------------------------------------------------------------
# In this tutorial we add some real-time graphics
# Observe we have imported matplotlib.pyplot (https://matplotlib.org/api/pyplot_api.html)
#----------------------------------------------------------------
class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.period_start = 3  # The start of a period
Event.update = 4        # Stuff that happens in the periode

# The Settings object
#---------------------------
# We have two new settings. The graphics i shown every periodes_per_pic periode.
# It is important for performance that periodes_per_pic >> 1
class Settings: pass
Settings.number_of_agents=0
Settings.number_of_periods=0
Settings.probability_of_death=0
Settings.number_of_new_born=0
Settings.out_file=""
Settings.graphics_show=False             # A new setting
Settings.graphics_periodes_per_pic=1     # A new setting

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._age = 0

    def event_proc(self, id_event):
        if id_event == Event.update:
            self._age += 1
            if random.random() < Settings.probability_of_death:
                self.remove_this_agent()

    def get_age(self):
        return self._age

#---------------------------
# The Statistics object
#---------------------------
# The graphics is initalized under Event.start (#1)
# The graphics is generated and shown under Event.periode_start (#2)
# A crude animation effect is gained by using plt.pause(0.0001) (#3)
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:
            self._file = open(Settings.out_file, "w")

            if Settings.graphics_show:                  #1
                plt.ion()
                plt.figure(figsize=[8,5])
                self._x, self._y = [], []

        elif id_event == Event.stop:
            self._file.close()

        elif id_event == Event.period_start:
            print(Simulation.population.get_number_of_agents())
            self._file.write("{}\t{}\n".format(Simulation.time, Simulation.population.get_number_of_agents()))

            if Settings.graphics_show:                  #2
                self._x.append(Simulation.time)
                self._y.append(Simulation.population.get_number_of_agents())
                if Simulation.time % Settings.graphics_periodes_per_pic==0:
                    plt.clf()
                    plt.plot(self._x, self._y, color="red", linewidth=0.25)
                    plt.axis(xmin=0,xmax=Settings.number_of_periods,
                             ymin=0 , ymax=1.2*Settings.number_of_agents)
                    plt.title("Number of persons")
                    plt.show()
                    plt.pause(0.0001)                   #3

class Simulation(Agent):
    # Static fields
    population = Agent()
    time = 0

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents

        # Simulation has two children:
        self._statistics = Statistics(self)
        Simulation.population = Agent(self)

        # Adding persons to the population
        for i in range(Settings.number_of_agents):
            Person(Simulation.population)

        # Start the simulation
        self.event_proc(Event.start)

    def event_proc(self, id_event):
        if id_event == Event.start:
            # Send Event.start down the tree to all decendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation   #2
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.period_start)
                self.event_proc(Event.update)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.stop)

        elif id_event == Event.update:
            # Adding new born persons to the population
            for i in range(Settings.number_of_new_born):
                Person(Simulation.population)
            super().event_proc(id_event)
        else:
            # All other events are sendt to decendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------
Settings.number_of_agents = 500
Settings.number_of_periods = 2000
Settings.probability_of_death = 0.01
Settings.number_of_new_born = 5
Settings.out_file = "test.txt"
Settings.graphics_show = True
Settings.graphics_periodes_per_pic = 25

Simulation()



