import random
from enum import Enum

from dream_agent import Agent


# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period
    UPDATE = 3        # Stuff that happens in the period

# The Settings object
#---------------------------
class Settings: pass # Defined later

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._wealth = 1  

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            if self._wealth >= 1:
                p = Simulation.population.get_random_agent(self)
                if random.random() < Settings.probability_give:
                    self.transfer_to(p, 1)

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

        if id_event == Event.PERIOD_START:
            # Collect data
            agent_wealths = [p.wealth for p in Simulation.population] 
            
            # calculate gini
            gini = compute_gini(agent_wealths, Settings.number_of_agents)
            
            # print to terminal 
            print("{}\t{}".format(Simulation.time, gini))

def compute_gini(wealths, N): # How to calculate gini
    x = sorted(wealths)
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B) 



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
Settings.number_of_agents = 100
Settings.number_of_periods = 1000
Settings.probability_give = 0.3

Simulation()


