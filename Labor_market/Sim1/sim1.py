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

# Communication
#---------------------------
class ECommunication(Enum):
    DO_YOU_HAVE_A_JOB = 0 
    I_QUIT = 1
    YES = 2         
    NO = 3         
    OK = 4

# The Settings object
#---------------------------
class Settings: pass # Defined later

# The Workers object
#---------------------------
class Worker(Agent):

    def __init__(self, parent=None, S=0, workplace=None):
        super().__init__(parent)
        self._S = S
        self._n = int(np.floor(S))         # Number of jobs to apply for
        self._prob = S - np.floor(S)  # Probability of extra job application
        self._workplace = workplace
        self._utility=0
        self._utility_discounted=0

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            if self._workplace==None: # If no job
                n = self._n
                if random.random() < self._prob: n=n+1
                for wp in Simulation.workplaces.get_random_agent(n=n):                        
                    if wp.communicate(ECommunication.DO_YOU_HAVE_A_JOB, self)==ECommunication.YES:
                        self._workplace = wp
                        break
            else: #If job: maybe quit
                if random.random() < Settings.worker_delta:
                    self._workplace.communicate(ECommunication.I_QUIT, self)
                    self._workplace = None                                            
           
            
            # Calculate utility
            if self._workplace==None: 
                self._utility = Simulation.benefits - Settings.worker_disutility * self._S  # If not working
            else:
                self._utility = Simulation.wage                             

            self._utility_discounted = Settings.worker_beta * self._utility_discounted + self._utility 

    @property
    def S(self):
        return self._S

    @property
    def workplace(self):
        return self._workplace

    @property
    def utility_discounted(self):
        return self._utility_discounted

# The Workplace object
#---------------------------
class Workplace(Agent):

    def __init__(self, parent=None, gamma=0, L=0):
        super().__init__(parent)
        self._gamma = gamma
        self._L = L

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            zz=22

    def communicate(self, e_communication, worker):
        return ECommunication.OK

    @property
    def gamma(self):
        return self._gamma

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        self._L = value


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
    time=0
    workers = Agent()
    workplaces = Agent()
    wage=0
    price=0
    benefits=0

    def __init__(self):
        super().__init__()
        self._statistics = Statistics(self)
        Simulation.workers = Agent(self)
        Simulation.workplaces = Agent(self)

        # Allocating workplaces and workers       
        for _ in range(Settings.number_of_workplaces):
            wp = Workplace(Simulation.workplaces, random.random()*Settings.workplace_max_gamma)   # Start with random gamma
            L=0
            for _ in range(Settings.number_of_workers_per_workplace):
                if random.random() < Settings.worker_probability_job_init:
                    Worker(Simulation.workers, random.random()*Settings.worker_max_S, wp)    # Job. Start with random S
                    L=L+1
                else:
                    Worker(Simulation.workers, random.random()*Settings.worker_max_S, None)  # No job. Start with random S
            wp.L = L

        # Initializing macro variables
        Simulation.wage = 1
        Simulation.price = 1
        Simulation.benefits = 0.5        

        # Start the simulation
        self.event_proc(Event.START)

    def event_proc(self, id_event):
        if id_event == Event.START:
            # Send Event.start down the tree to all defendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation
            while Simulation.time < Settings.number_of_periods:
                # Important when agents are searching
                Simulation.workplaces.randomize_agents()           
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
Settings.number_of_workplaces = 100
Settings.number_of_workers_per_workplace = 10


Settings.worker_max_S = 10 # maximum number of job search
Settings.worker_probability_job_init = 0.9 # Probability of having job when the model starts
Settings.worker_beta = 0.95 # Discounting factor
Settings.worker_disutility = 0.1
Settings.worker_delta = 0.05 # Probability of quitting job
Settings.workplace_max_gamma = 1.0 # maximum gamma
Settings.workplace_beta = 0.95 # Discounting factor


Settings.number_of_periods = 100

Settings.graphics_periods_per_pic = 10


Simulation()


