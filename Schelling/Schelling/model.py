import random
import matplotlib.pyplot as plt
import math
import os

from dream_agent import *

from .enums import *
from .settings import *
from .plots import *

#---------------------------

class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._type = EType.MAJORITY if random.random() < Settings.person_density_of_majority else EType.MINORITY
        self._x = random.random()
        self._y = random.random()

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            while not self.nice_location(self._x, self._y):
                self._x = random.random()
                self._y = random.random()
    
    def nice_location(self, x, y):
        n = len(Simulation.population)
        dist = [0]*n 
        same = [0]*n 
        i=0
        for p in Simulation.population:
            dist[i] = math.sqrt((x - p._x)**2 + (y - p._y)**2)
            same[i] = int(self._type==p.type)
            i += 1 

        dist, same = (list(t) for t in zip(*sorted(zip(dist, same)))) # sort dist and same after dist
        n_same = sum(same[:Settings.person_n_nearest])

        share = n_same/Settings.person_n_nearest
        
        return share >= Settings.person_share_ok
    
    @property
    def type(self):
        return self._type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

#---------------------------

class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics           

        elif id_event == Event.PERIOD_START:
            show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
            last_periode = Simulation.time == Settings.number_of_periods-1            
            if show_pic or last_periode:

                # Collect data
                minority_x, minority_y = [], [] 
                majority_x, majority_y = [], [] 
                for p in Simulation.population:
                    if p.type==EType.MAJORITY:
                        majority_x.append(p.x)                  
                        majority_y.append(p.y)
                    else:
                        minority_x.append(p.x)                  
                        minority_y.append(p.y)

                plt.clf()
                plot1(minority_x, minority_y, majority_x, majority_y, t=Simulation.time)
                plt.show()

                if show_pic and not last_periode: 
                    plt.pause(1e-1) # Crude animation
                    # print("--------------------------") 

                if last_periode:    
                    file = Settings.graphics_file
                    plt.savefig(file)
                    os.system("start " + file)

            # print to terminal 
            print("{}".format(Simulation.time))

    
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
        for _ in range(Settings.person_number_of):
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

Simulation()


