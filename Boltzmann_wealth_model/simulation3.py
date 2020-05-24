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

# The Settings object
#---------------------------
class Settings: pass # Defined later

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None, x=0, y=0):
        super().__init__(parent)
        self._wealth = 1
        self._x, self._y = Simulation.grid_append(x, y, self)

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            # Wealth-giving
            if self._wealth >= 1:
                g = Simulation.grid[self._x][self._y].copy()
                if len(g) > 1:
                    g.remove(self)  # You don't want to give money to yourself    
                    p = random.choice(g)        # Choose a random person
                    if random.random() < Settings.probability_give:
                        self.transfer_to(p, 1)  # Give money

            # Moving
            if random.random() < Settings.probability_move:
                # Move to random neighbor cell in the grid
                d_xy = random.choice([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]])
                self._x, self._y = Simulation.grid_move(self._x + d_xy[0], self._y + d_xy[1], self)

    def transfer_to(self, other, value):                     
        self._wealth -= value
        other._wealth += value

    @property
    def wealth(self):
        return self._wealth

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
            graphics_init() # Initialize graphics
            
            self._personRandom = None # A random person to follow
            
            # Initialize time series data
            self._gini = []   
            self._wealthRandom = []         

        elif id_event == Event.PERIOD_START:
            # If _personRandom is not defines, choose a random person
            if self._personRandom==None: self._personRandom = Simulation.population.get_random_agent()

            # Collect data
            agent_wealths = [p.wealth for p in Simulation.population] 
            self._wealthRandom.append(self._personRandom.wealth)

            n_agents = np.zeros((Settings.grid_size_x, Settings.grid_size_y))
            for x in range(Settings.grid_size_x):
                for y in range(Settings.grid_size_y):
                    n_agents[x][y] = len(Simulation.grid[x][y])

            # calculate gini
            gini = compute_gini(agent_wealths)
            self._gini.append(gini) # Add to time series

            # Show real time graphics (every graphics_periods_per_pic periode)
            if Simulation.time % Settings.graphics_periods_per_pic==0:
                graphics_define(x1=self._gini, x2=agent_wealths, x3=self._wealthRandom, x4=n_agents, title="Gini coefficient [t: {}]".format(Simulation.time))
                plt.show()
                plt.pause(1e-6) # Crude animation

            # Final pic open for 15 sec. and saved
            if Simulation.time == Settings.number_of_periods-1:
                graphics_define(x1=self._gini, x2=agent_wealths, x3=self._wealthRandom, x4=n_agents, title="Gini coefficient")
                plt.savefig("Boltzmann_wealth_model//graphics//simulation3.png")
                plt.pause(15)

def compute_gini(wealths): # How to calculate gini
    N = len(wealths)
    x = sorted(wealths)
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B) 

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,8])

def graphics_define(x1, x2, x3, x4, title=""):
    plt.clf()
    
    plt.subplot(2,2,1)
    plt.title(title)
    plt.plot(x1)
    #plt.xlabel("Periods")
    plt.ylabel("Gini")
    plt.xlim(0, Settings.number_of_periods) 
    plt.ylim(0.0, 1.0) 

    plt.subplot(2,2,2)
    plt.title("Histogram of wealth")
    plt.hist(x2, bins = range(10), align='left', rwidth=0.3)
    #plt.xlabel("Wealth")
    plt.ylabel("Number")
    plt.xlim(-0.2, 9) 
    #plt.ylim(0.0, 1.0) 

    plt.subplot(2,2,3)
    plt.title("Random persons wealth")
    plt.plot(x3)
    plt.xlabel("Periods")
    plt.ylabel("Wealth")
    plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(0.0, 1.0) 

    plt.subplot(2,2,4)
    plt.title("Grid")
    plt.imshow(x4, interpolation='nearest')
    plt.colorbar()
    
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
        Simulation.grid = [[[] for x in range(Settings.grid_size_x)] 
                               for y in range(Settings.grid_size_y)]

        # Adding persons to the population
        for _ in range(Settings.number_of_agents):
            x = random.randint(0, Settings.grid_size_x - 1)
            y = random.randint(0, Settings.grid_size_y - 1)
            Person(Simulation.population, x=x, y=y)

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

        Simulation.grid[x_new][y_new].append(p)

        return x_new, y_new            

    @staticmethod
    def grid_move(x , y, p):
        # Make sure that x, y is inside the grid
        x_new = x % Settings.grid_size_x
        y_new = y % Settings.grid_size_y

        Simulation.grid[p.x][p.y].remove(p)      # remove fom old place
        Simulation.grid[x_new][y_new].append(p)  # move to new place

        return x_new, y_new            


# We can now run the model
#--------------------------
Settings.number_of_agents = 250
Settings.number_of_periods = 500
Settings.probability_give = 0.1
Settings.probability_move = 0.5
Settings.graphics_periods_per_pic = 10

Settings.grid_size_x = 10
Settings.grid_size_y = 10

Simulation()


