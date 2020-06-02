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


class Household(Agent):
    
    def __init__(self, parent=None): # Important to add default values. Here age=0
        super().__init__(parent)

    def event_proc(self, id_event):
        if id_event == Event.PERIOD_STOP: 
            return

        elif id_event == Event.UPDATE:
            return                

        elif id_event == Event.PERIOD_STOP:
            return

    def communicate(self, e_communication, person):
        if e_communication==ECommunication.HI:
            return ECommunication.HI




class Firm(Agent):
    
    def __init__(self, parent=None, age=0): # Important to add default values. Here age=0
        super().__init__(parent)
        if Simulation.time==-1:  # The model has not started yet
            self._wage = math.exp(random.gauss(Settings.firm_init_wage_mean, Settings.firm_init_wage_sd))   
        else:
            self._wage = 1

    def event_proc(self, id_event):
        if id_event == Event.START: 
            return

        elif id_event == Event.PERIOD_START: 
            return

        elif id_event == Event.UPDATE:
            return
   
        elif id_event == Event.PERIOD_STOP:
            return

    def communicate(self, e_communication, person):
        if e_communication==ECommunication.HI:
            return ECommunication.HI


    @property
    def wage(self):
        return self._wage

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
            wage = [f.wage for f in Simulation.firms] 

            # Show real time graphics (every graphics_periods_per_pic periode)
            show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
            last_periode = Simulation.time == Settings.number_of_periods-1            
            if show_pic or last_periode:
                plt.clf()
                plot1(self._N_households)
                plot2(wage)
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
    


class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    time=-1 # If time=-1 the model has not started yet.
    households=None
    firms=None

    def __init__(self):
        super().__init__()
        if Settings.random_seed>0:
            random.seed(Settings.random_seed)

        Simulation.statistics = Statistics(self)
        Simulation.households = Agent(self)
        Simulation.firms = Agent(self)

        # Allocating agents       
        for _ in range(Settings.number_of_households):
            Household(Simulation.households)

        for _ in range(Settings.number_of_firms):
            Firm(Simulation.firms)


        # Start the simulation
        self.event_proc(Event.START)


    def event_proc(self, id_event):
        if id_event == Event.START:
            # Send Event.start down the tree to all defendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation
            Simulation.time=0
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





