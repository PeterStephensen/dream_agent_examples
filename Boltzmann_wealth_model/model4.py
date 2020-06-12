from dream_agent import Agent
import os
from enum import Enum
import random
import matplotlib.pyplot as plt

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period
    UPDATE = 3        # Stuff that happens in the period

# Communication
#---------------------------
class ECommunication(Enum):
    DO_YOU_WANT_SOME_MONEY  = 0
    YES = 1
    NO = 2

# The Settings object
#---------------------------
class Settings: pass # Defined later

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._wealth = 1
        self._friends = None # Friends can not be allocated here, as all persons are not allocated yet   

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            if self._friends == None: 
                self._friends = Simulation.population.get_random_agent(self, n=Settings.number_of_friends)
            
            if self._wealth >= 1:
                f = random.choice(self._friends) # A random friends
                if f.communicate(ECommunication.DO_YOU_WANT_SOME_MONEY, self) == ECommunication.YES:
                    self.transfer_to(f, 1)

    def communicate(self, e_communication, person):
        if random.random() < Settings.probability_YES:
            return ECommunication.YES
        else:
            return ECommunication.NO
    
    def transfer_to(self, other, value):                     
        self._wealth -= value
        other._wealth += value

    @property
    def wealth(self):
        return self._wealth


# The Statistics object
#---------------------------
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._gini = [] # Initialize time series data           

        elif id_event == Event.PERIOD_START:
            # Collect data
            agent_wealths = [p.wealth for p in Simulation.population] 
            
            # calculate gini
            gini = compute_gini(agent_wealths)
            self._gini.append(gini) # Add to time series

            # Show real time graphics (every graphics_periods_per_pic periode)
            if Simulation.time % Settings.graphics_periods_per_pic==0:
                graphics_define(x=self._gini, title="Gini coefficient [t: {}]".format(Simulation.time))
                plt.show()
                plt.pause(1e-6) # Crude animation

            # Final pic open for 15 sec. and saved
            if Simulation.time == Settings.number_of_periods-1:
                graphics_define(x=self._gini, title="Gini coefficient")
                plt.savefig("Boltzmann_wealth_model//graphics//simulation4.png")
                plt.pause(15)

def compute_gini(wealths): # How to calculate gini
    N = len(wealths)
    x = sorted(wealths)
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B) 

def graphics_init():
    plt.ion()        # Necessary to get animation effect
    plt.figure(figsize=[10,5])

def graphics_define(x, title=""):
    plt.clf()
    plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Gini")
    plt.xlim(0, Settings.number_of_periods) 
    plt.ylim(0, 1) 

# The Simulation object
#---------------------------
class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    population = Agent()
    time = 0

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents

        # Simulation has two children:
        self._statistics = Statistics(self)
        Simulation.population = Agent(self)

        # Adding persons to the population
        for _ in range(Settings.number_of_agents):
            Person(Simulation.population)

        # Start the simulation
        self.event_proc(Event.START)

    def event_proc(self, id_event):
        if id_event == Event.START:
            # Send Event.start down the tree to all defendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation
            while Simulation.time < Settings.number_of_periods:
                # Important when agents are searching
                Simulation.population.randomize_agents()           
                self.event_proc(Event.PERIOD_START)
                self.event_proc(Event.UPDATE)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.STOP)

        else:
            # All other events are send to defendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------
Settings.number_of_agents = 1000
Settings.number_of_periods = 500
Settings.probability_give = 0.1
Settings.graphics_periods_per_pic = 10

Settings.number_of_friends = 10
Settings.probability_YES = 0.8

Simulation()


