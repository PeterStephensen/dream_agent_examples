import random
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os
import time

from dream_agent import Agent

from enums import Event, ECommunication   
from settings import Settings
from plots import graphics_init
from plots import plot1, plot2

# The Household object
#---------------------------
class Household(Agent):
    
    def __init__(self, parent=None, age=0): # Important to add default values. Here age=0
        super().__init__(parent)
        self._age = age

    def event_proc(self, id_event):
        # Behavior in the start of the period. Here: Nothing implemented
        if id_event == Event.PERIOD_STOP: 
            return

        # Behavior during the periode: Here: You get one period older  
        elif id_event == Event.UPDATE:
            self._age += 1

            my = math.exp(-10 + 0.1*self._age)  # probability og death
            if random.random() < my:
                self.remove_this_agent()        # If dead: remove!
    
        # Behavior in the end of the period. Here: Nothing implemented
        elif id_event == Event.PERIOD_STOP:
            return

    # Communication. Here: if a person contacts you and says HI, you answer HI
    def communicate(self, e_communication, person):
        if e_communication==ECommunication.HI:
            return ECommunication.HI


    @property
    def age(self):
        return self._age


# The Firm object
#---------------------------
class Firm(Agent):
    
    def __init__(self, parent=None, age=0): # Important to add default values. Here age=0
        super().__init__(parent)
        self._age = age

    def event_proc(self, id_event):
        # Behavior in the start of the period. Here: Nothing implemented
        if id_event == Event.PERIOD_STOP: 
            return

        # Behavior during the periode: Here: You get one period older  
        elif id_event == Event.UPDATE:
            self._age += 1

   
        # Behavior in the end of the period. Here: Nothing implemented
        elif id_event == Event.PERIOD_STOP:
            return

    # Communication. Here: if a person contacts you and says HI, you answer HI
    def communicate(self, e_communication, person):
        if e_communication==ECommunication.HI:
            return ECommunication.HI


    @property
    def age(self):
        return self._age


# The Statistics object
#---------------------------
class Statistics(Agent):
    
    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._N_households = []
            self._time = None
            self._time_total = time.time()


        elif id_event == Event.PERIOD_START:
            # Collect time series data
            self._N_households.append(len(Simulation.households))
            age = [h.age for h in Simulation.households] 

            # Show real time graphics (every graphics_periods_per_pic periode)
            show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
            last_periode = Simulation.time == Settings.number_of_periods-1            
            if show_pic or last_periode:
                plt.clf()
                plot1(self._N_households)
                plot2(age)
                plt.show()

                if show_pic and not last_periode: 
                    plt.pause(1e-1) # Crude animation
                    print("--------------------------") 

                if last_periode:    # Final pic open for 15 sec. and saved
                    now = datetime.now()
                    file = Settings.graphics_file
                    plt.savefig(file)
                    os.system("start " + file)

            # print to terminal 
            if self._time is not None:
                print("{}\t{:.4f} sec.".format(Simulation.time, time.time() - self._time))

            self._time = time.time()

        elif id_event == Event.STOP:
            print("--------------------------")
            print("Total time use: {:.2f} sec.".format(time.time() - self._time_total))
            print("--------------------------")
    


# The Simulation object
#---------------------------
class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    time=0
    households=None


    def __init__(self):
        super().__init__()
        if Settings.random_seed>0:
            random.seed(Settings.random_seed)

        Simulation.statistics = Statistics(self)
        Simulation.households = Agent(self)

        # Allocating persons. Here: Age between 0 and 50       
        for _ in range(Settings.number_of_households):
            Household(Simulation.households, age=random.randint(0,50))

        # Start the simulation
        self.event_proc(Event.START)


    def event_proc(self, id_event):
        if id_event == Event.START:
            # Send Event.start down the tree to all defendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.PERIOD_START)
                self.event_proc(Event.UPDATE)
                self.event_proc(Event.PERIOD_STOP)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.STOP)

        # if id_event == Event.PERIOD_STOP:
        #     super().event_proc(id_event)
    
        # if id_event == Event.STOP:
        #     super().event_proc(id_event)


        else:
            # All other events are send to defendants
            super().event_proc(id_event)

# We can now run the model
#--------------------------
Simulation()





