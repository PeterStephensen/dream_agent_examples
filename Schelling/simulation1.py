from dream_agent import Agent
from enum import Enum
import random
import matplotlib.pyplot as plt
import numpy as np

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period
    UPDATE = 3        # Stuff that happens in the period

# Agent types
#---------------------------
class EType(Enum):
    MAJORITY = 0
    MINORITY = 1


# The Settings object
#---------------------------
class Settings: pass # Defined later

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None, x=0, y=0, type=EType.MAJORITY):
        super().__init__(parent)
        self._type = type
        self._x, self._y = Simulation.grid_append(x, y, self)

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            similar = 0
            # for p in Simulation.grid[self._x][self._y]:

            # Moving
            # if random.random() < Settings.probability_move:
            #     # Move to random neighbor cell in the grid
            #     d_xy = random.choice([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]])
            #     self._x, self._y = Simulation.grid_move(self._x + d_xy[0], self._y + d_xy[1], self)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

# The Statistics object
#---------------------------
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            zzz=222
            #graphics_init() # Initialize graphics
            

        elif id_event == Event.PERIOD_START:
            # Collect data

            # calculate gini

            # Show real time graphics (every graphics_periods_per_pic periode)
            # if Simulation.time % Settings.graphics_periods_per_pic==0:
            #     graphics_define(x1=self._gini, x2=agent_wealths, x3=self._wealthRandom, x4=n_agents, title="Gini coefficient [t: {}]".format(Simulation.time))
            #     plt.show()
            #     plt.pause(1e-6) # Crude animation

            # Final pic open for 15 sec. and saved
            # if Simulation.time == Settings.number_of_periods-1:
            #     graphics_define(x1=self._gini, x2=agent_wealths, x3=self._wealthRandom, x4=n_agents, title="Gini coefficient")
            #     plt.savefig("Boltzmann_wealth_model//graphics//simulation3.png")
            #     plt.pause(15)

            # print to terminal 
            print("{}".format(Simulation.time))


def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,8])

def graphics_define(x1, x2, x3, x4, title=""):
    plt.clf()
    
    # plt.subplot(2,2,1)
    # plt.title(title)
    # plt.plot(x1)
    # #plt.xlabel("Periods")
    # plt.ylabel("Gini")
    # plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0.0, 1.0) 

    # plt.subplot(2,2,2)
    # plt.title("Histogram of wealth")
    # plt.hist(x2, bins = range(10), align='left', rwidth=0.3)
    # #plt.xlabel("Wealth")
    # plt.ylabel("Number")
    # plt.xlim(-0.2, 9) 
    # #plt.ylim(0.0, 1.0) 

    # plt.subplot(2,2,3)
    # plt.title("Random persons wealth")
    # plt.plot(x3)
    # plt.xlabel("Periods")
    # plt.ylabel("Wealth")
    # plt.xlim(0, Settings.number_of_periods) 
    # #plt.ylim(0.0, 1.0) 

    # plt.subplot(2,2,4)
    # plt.title("Grid")
    # plt.imshow(x4, interpolation='nearest')
    # plt.colorbar()
    
# The Simulation object
#---------------------------
class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    population = Agent()
    time = 0
    grid = None

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents

        # Simulation has two children:
        self._statistics = Statistics(self)
        Simulation.population = Agent(self)

        # Allocating the grid
        Simulation.grid = [[None for x in range(Settings.grid_size_x)] 
                                 for y in range(Settings.grid_size_y)]

        # Adding persons to the population       
        for x in range(Settings.grid_size_x):
            for y in range(Settings.grid_size_y):
                if random.random() < Settings.density_of_agents:                    
                    t = EType.MINORITY
                    if random.random() < Settings.density_of_majority: t = EType.MAJORITY
                    Person(Simulation.population, x=x, y=y, type=t)

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

    @staticmethod
    def grid_append(x , y, p):
        # Make sure that x, y is inside the grid
        x_new = x % Settings.grid_size_x
        y_new = y % Settings.grid_size_y

        Simulation.grid[x_new][y_new] = p

        return x_new, y_new            

    # @staticmethod
    # def grid_move(x , y, p):
    #     # Make sure that x, y is inside the grid
    #     x_new = x % Settings.grid_size_x
    #     y_new = y % Settings.grid_size_y

    #     Simulation.grid[p.x][p.y].remove(p)      # remove fom old place
    #     Simulation.grid[x_new][y_new].append(p)  # move to new place

    #     return x_new, y_new            


# We can now run the model
#--------------------------
Settings.density_of_agents = 0.75
Settings.number_of_periods = 500

Settings.density_of_majority = 0.75


Settings.graphics_periods_per_pic = 10

Settings.grid_size_x = 10
Settings.grid_size_y = 10

Simulation()


