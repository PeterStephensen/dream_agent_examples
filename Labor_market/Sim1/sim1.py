import random
import matplotlib.pyplot as plt
import math

from dream_agent import Agent
from enums import *
from settings import *
from plots import *

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
        self._unemployment_duration=0

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            if self._workplace==None: # If no job
                n = self._n
                if random.random() < self._prob: n += 1

                for wp in Simulation.workplaces.get_random_agents(n=n):                        
                    if wp.communicate(ECommunication.DO_YOU_HAVE_A_JOB, self)==ECommunication.YES:
                        self._workplace = wp
                        break
            else: #If job: maybe quit
                if random.random() < Settings.worker_delta:
                    self._workplace.communicate(ECommunication.I_QUIT, self)
                    self._workplace = None                                            

            if self._workplace==None:
                self._unemployment_duration += 1
            else:
                self._unemployment_duration = 0


        if id_event == Event.PERIOD_STOP:

            # Calculate utility
            if self._workplace==None: 
                self._utility = Simulation.benefits * math.exp(- Settings.worker_eta * self._S)  # If not working
            else:
                self._utility = Simulation.wage                             

            self._utility_discounted = Settings.worker_beta * self._utility_discounted\
            + self._utility ** (1-Settings.worker_rho) / (1-Settings.worker_rho)



    @property
    def S(self):
        return self._S

    @property
    def workplace(self):
        return self._workplace

    @property
    def utility_discounted(self):
        return self._utility_discounted

    @property
    def unemployment_duration(self):
        return self._unemployment_duration


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
            Y = self._A ** (1-Settings.workplace_alpha) * (self._theta / Settings.workplace_alpha)\
                 * self._L ** Settings.workplace_alpha

            self._profit = Simulation.price * Y - Simulation.wage * self._L\
                 - Settings.workplace_kappa * self._V
            
            self._profit_discounted = Settings.workplace_beta * self._profit_discounted + self._profit

            self._theta = math.exp(math.log(self._theta) + random.gauss(0, Settings.workplace_sigma))


    def communicate(self, e_communication, worker):
        if e_communication==ECommunication.DO_YOU_HAVE_A_JOB:
            if self._hired < self._V:
                self._hired = self._hired + 1
                self._L = self._L + 1 
                return ECommunication.YES
            else:
                return ECommunication.NO

        elif e_communication==ECommunication.I_QUIT:
            #self._hired = self._hired - 1
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

    @property
    def profit_discounted(self):
        return self._profit_discounted


# The Statistics object
#---------------------------
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._L_tot = []          

        elif id_event == Event.PERIOD_START:
            # Collect time series data
            L = [wp.L for wp in Simulation.workplaces] 
            self._L_tot.append(sum(L))

            # Show real time graphics (every graphics_periods_per_pic periode)
            show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
            last_periode = Simulation.time == Settings.number_of_periods-1            
            if show_pic or last_periode:
                # Collect data for cross section
                gamma = [wp.gamma for wp in Simulation.workplaces] 
                profit_discounted = [wp.profit_discounted for wp in Simulation.workplaces] 
                S = [w.S for w in Simulation.workers] 
                utility_discounted = [w.utility_discounted for w in Simulation.workers] 
                unemployment_duration = [w.unemployment_duration for w in Simulation.workers 
                                         if w.workplace==None] 

                plt.clf()
                plot1(self._L_tot)
                plot2(gamma, profit_discounted)
                plot3(S, utility_discounted)
                plot4(L)
                plot5(unemployment_duration)
                plt.show()

                if show_pic: 
                    plt.pause(1e-6) # Crude animation

                if last_periode:    # Final pic open for 15 sec. and saved
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
        if Settings.random_seed>0:
            random.seed(Settings.random_seed)
        
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
                    Worker(Simulation.workers, S_min + random.random()*d_S, None)  # No job. Start with random S

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
                self.event_proc(Event.PERIOD_START)
                self.event_proc(Event.UPDATE)
                self.event_proc(Event.PERIOD_STOP)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.STOP)
        
        elif id_event == Event.UPDATE:
            # if Simulation.time == 100:       # Shock to the price level
            #     Simulation.price = 0.9
            super().event_proc(id_event)

        else:
            # All other events are send to defendants
            super().event_proc(id_event)



# We can now run the model
#--------------------------
Simulation()

