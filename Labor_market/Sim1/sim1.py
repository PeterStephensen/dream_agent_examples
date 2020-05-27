from enum import Enum
import random
import matplotlib.pyplot as plt
import math

from dream_agent import Agent
from settings import Settings
from plots import *

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period. Statistics register data
    PERIOD_STOP = 4   # The start of a period. Agents calculate utility and profits
    UPDATE = 4        # Stuff that happens in the period

# Communication
#---------------------------
class ECommunication(Enum):
    DO_YOU_HAVE_A_JOB = 0 
    I_QUIT = 1
    YES = 2         
    NO = 3         
    OK = 4


# The Workers object
#---------------------------
class Worker(Agent):

    def __init__(self, parent=None, S=0, workplace=None):
        super().__init__(parent)
        self._S = S
        self._n = int(math.floor(S))         # Number of jobs to apply for
        self._prob = S - math.floor(S)  # Probability of extra job application
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

        if id_event == Event.PERIOD_STOP:
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
        self._V = 0
        self._N_hat = 0
        self._hired = 0
        self._theta = 1
        self._profit=0
        self._profit_discounted=0

        # Calibration af A
        self._A = Settings.number_of_workers_per_workplace * Settings.worker_probability_job_init

    def event_proc(self, id_event):
        if id_event == Event.PERIOD_START:
            L_hat = self._A * (self._theta /(Simulation.wage / Simulation.price)) ** (1/(1-Settings.workplace_alpha))
            N_hat = L_hat - (1 - Settings.worker_delta) * self._L
            self._V = self._gamma * N_hat
            self._hired=0

#        elif id_event == Event.UPDATE:

        elif id_event == Event.PERIOD_STOP:
            Y = self._A ** (1-Settings.workplace_alpha) * (self._theta / Settings.workplace_alpha) * self._L ** Settings.workplace_alpha
            self._profit = Simulation.price * Y - Simulation.wage * self._L - Settings.workplace_kappa * self._V
            self._profit_discounted = Settings.workplace_beta * self._profit_discounted + self._profit

            self._theta = math.exp(math.log(self._theta) + random.gauss(0, Settings.workplace_sigma))
            if (Simulation.time > 50) & (self._profit_discounted<-10000):
                L_hat = self._A * (self._theta /(Simulation.wage / Simulation.price)) ** (1/(1-Settings.workplace_alpha))
                N_hat = L_hat - (1 - Settings.worker_delta) * self._L
                zz=22

    def communicate(self, e_communication, worker):
        if e_communication==ECommunication.DO_YOU_HAVE_A_JOB:
            if self._hired < self._V:
                self._hired = self._hired + 1
                self._L = self._L + 1 
                return ECommunication.YES
            else:
                return ECommunication.NO

        elif e_communication==ECommunication.I_QUIT:
            self._hired = self._hired - 1
            self._L = self._L - 1 
            return ECommunication.OK


    def add_worker(self):
        self._L=self._L+1

    @property
    def gamma(self):
        return self._gamma

    @property
    def L(self):
        return self._L


# The Statistics object
#---------------------------
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._L_tot = []          

        elif id_event == Event.PERIOD_START:
            # Collect data
            L = [wp.L for wp in Simulation.workplaces] 
            gamma = [wp.gamma for wp in Simulation.workplaces] 
            profit_discounted = [wp._profit_discounted for wp in Simulation.workplaces] 
            S = [w.S for w in Simulation.workers] 
            utility_discounted = [w.utility_discounted for w in Simulation.workers] 

            self._L_tot.append(sum(L))

            # Show real time graphics (every graphics_periods_per_pic periode)
            if Simulation.time % Settings.graphics_periods_per_pic==0:
                plt.clf()
                plot1(self._L_tot)
                # plot2(gamma, profit_discounted)
                plot2(gamma, L)
                plot3(S, utility_discounted)
                plot4(L)
                plt.show()
                plt.pause(1e-6) # Crude animation

            # Final pic open for 15 sec. and saved
            if Simulation.time == Settings.number_of_periods-1:
                plt.clf()
                plot1(self._L_tot)
                # plot2(gamma, profit_discounted)
                plot2(gamma, L)
                plot3(S, utility_discounted)
                plot4(L)
                plt.savefig("Labor_market//Sim1//graphics//sim1.png")
                plt.pause(15)

            # print to terminal 
            print("{}\t{}".format(Simulation.time, sum(L)))


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
        gamma_min = Settings.workplace_min_gamma
        d_gamma = Settings.workplace_max_gamma - gamma_min
        S_min = Settings.worker_min_S
        d_S = Settings.worker_max_S - S_min
        for _ in range(Settings.number_of_workplaces):
            wp = Workplace(Simulation.workplaces, gamma_min + random.random()*d_gamma)   # Start with random gamma
            for _ in range(Settings.number_of_workers_per_workplace):
                if random.random() < Settings.worker_probability_job_init:
                    Worker(Simulation.workers, S_min + random.random()*d_S, wp)    # Job. Start with random S
                    wp.add_worker()
                else:
                    Worker(Simulation.workers, S_min + random.random()**d_S, None)  # No job. Start with random S

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
        
        elif id_event == Event.UPDATE:
            # if Simulation.time == 100:       # Shock to the price level
            #     Simulation.price = 0.5
            super().event_proc(id_event)

        else:
            # All other events are send to defendants
            super().event_proc(id_event)



# We can now run the model
#--------------------------
Simulation()


