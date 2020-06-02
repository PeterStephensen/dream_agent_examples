import random
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os

from dream_agent import Agent
from dream_agent import local_mean

from enums import Event, ECommunication   
from settings import Settings
from plots import graphics_init
from plots import plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8


# The Worker object
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

            # Learning
            if Settings.worker_learn:
                if random.random() < Settings.worker_learn_probabilily:
                    best_S = Simulation.statistics.best_S 
                    if best_S is not None:                    
                        adj = Settings.worker_learn_adjustment
                        self._S = (1 - adj)*self._S + adj*best_S

                if random.random() < Settings.worker_learn_probabilily_mutation:
                    a = random.random()
                    self._S = a * Settings.worker_min_S + (1-a) * Settings.worker_max_S



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

    def event_proc(self, id_event):
        if id_event == Event.PERIOD_START:
            A = Simulation.A
            p = Simulation.price
            w = Simulation.wage
            alpha = Settings.workplace_alpha
            kappa = Settings.workplace_kappa
            delta = Settings.worker_delta

            L_hat = (p*A*self._theta/(w + kappa*delta*self._gamma))**(1/(1-alpha))
            N_hat = L_hat - (1 -delta) * self._L
            if N_hat > 0:
                self._V = self._gamma * N_hat
                n = int(math.floor(self._V))
                prob = self._V - math.floor(self._V)
                if random.random() < prob: n += 1
                self._V = n                       
            else:
                self._V = 0                       
            
            self._hired=0

#        elif id_event == Event.UPDATE:

        elif id_event == Event.PERIOD_STOP:
            # Calculating profit and updating technology
            A = Simulation.A
            p = Simulation.price
            w = Simulation.wage
            alpha = Settings.workplace_alpha
            kappa = Settings.workplace_kappa
            beta = Settings.worker_beta
            delta = Settings.worker_delta

            Y = A * self._theta * self._L**alpha / alpha
            self._profit = p * Y - w * self._L - kappa * self._V         
            self._profit_discounted = beta * self._profit_discounted + self._profit

            # L_hat = (p*A*self._theta/(w + kappa*delta*self._gamma))**(1/(1-alpha))
            # N_hat = L_hat - (1 - delta) * self._L

            # if self._profit_discounted < -3000:
            #     zz=22

            self._theta = math.exp(math.log(self._theta) + random.gauss(0, Settings.workplace_sigma))

            # Learning
            if Settings.workplace_learn:
                if random.random() < Settings.workplace_learn_probabilily:
                    best_gamma = Simulation.statistics.best_gamma 
                    if best_gamma is not None:                    
                        adj = Settings.workplace_learn_adjustment
                        self._gamma = (1 - adj)*self._gamma + adj*best_gamma                        

                if random.random() < Settings.workplace_learn_probabilily_mutation:
                    a = random.random()
                    self._gamma = a * Settings.workplace_min_gamma + (1-a) * Settings.workplace_max_gamma

    def communicate(self, e_communication, worker):
        if e_communication==ECommunication.DO_YOU_HAVE_A_JOB:
            if self._hired < self._V:
                self._hired += 1
                self._L += 1 
                return ECommunication.YES
            else:
                return ECommunication.NO

        elif e_communication==ECommunication.I_QUIT:
            self._L -= 1 
            return ECommunication.OK


    def add_worker(self):
        self._L += 1

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
            self._best_S_series = []
            self._best_gamma_series = []
            self._unemployed_series = []
            self._best_S=None          
            self._best_gamma=None          

        elif id_event == Event.PERIOD_START:
            # Collect time series data
            L = [wp.L for wp in Simulation.workplaces] 
            self._L_tot.append(sum(L))

            u = [1 for w in Simulation.workers if w.workplace is None] 
            self._unemployed_series.append(sum(u))

            self._best_S_series.append(self.best_S)
            self._best_gamma_series.append(self.best_gamma)


            if Simulation.time % Settings.statistics_update_learn==0:
                adj = Settings.statistics_update_learn_adjust
                if Settings.worker_learn:
                    S = [w.S for w in Simulation.workers] 
                    utility_discounted = [w.utility_discounted for w in Simulation.workers] 
                    s, u = local_mean(S, utility_discounted, n=Settings.worker_learn_n_points) 
                    if self._best_S is None:
                        self._best_S = s[u.index(max(u))]   
                    else:
                        self._best_S = adj * s[u.index(max(u))] + (1 - adj) * self._best_S

                if Settings.workplace_learn:
                    gamma = [wp.gamma for wp in Simulation.workplaces] 
                    profit_discounted = [wp.profit_discounted for wp in Simulation.workplaces] 
                    g, p = local_mean(gamma, profit_discounted, n=Settings.workplace_learn_n_points) 
                    if self._best_gamma is None:
                        self._best_gamma = g[p.index(max(p))]
                    else:    
                        self._best_gamma = adj * g[p.index(max(p))] + (1 - adj) * self._best_gamma

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
                plot5(self._unemployed_series)
                plot6(self._best_gamma_series)
                plot7(self._best_S_series)
                plot8(unemployment_duration)
                plt.show()

                if show_pic: 
                    plt.pause(1e-1) # Crude animation

                if last_periode:    # Final pic open for 15 sec. and saved
                    now = datetime.now()
                    file = "Labor_market//Sim1//graphics//sim1_{}.png".format(now.strftime("%m_%d_%Y__%H_%M_%S"))
                    plt.savefig(file)
                    plt.pause(1)
                    os.system("start " + file)






            # print to terminal 
            print("{}\t{}".format(Simulation.time, sum(L)))

    @property
    def best_S(self):
        return self._best_S

    @property
    def best_gamma(self):
        return self._best_gamma


# The Simulation object
#---------------------------
class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    time=0
    workers=None
    workplaces=None
    statistics=None
    wage=0
    price=0
    benefits=0
    A=0

    def __init__(self):
        super().__init__()
        if Settings.random_seed>0:
            random.seed(Settings.random_seed)
        
        Simulation.statistics = Statistics(self)
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

        # Calibration af A
        L = Settings.number_of_workers_per_workplace * Settings.worker_probability_job_init
        alpha = Settings.workplace_alpha
        kappa = Settings.workplace_kappa
        delta = Settings.worker_delta
        gamma = 0.5*(Settings.workplace_min_gamma + Settings.workplace_max_gamma)
        Simulation.A = L**(1-alpha) * (1 + kappa*gamma*delta)
        
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
            if (Simulation.time >= 100) and (Simulation.time <= 300):       # Shock to the price level
                Simulation.price = 0.95
                Settings.graphics_periods_per_pic = 1
            else:
                Simulation.price = 1.00

            super().event_proc(id_event)

        else:
            # All other events are send to defendants
            super().event_proc(id_event)

# We can now run the model
#--------------------------
Simulation()


