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
from plots import plot1, plot2, plot3


class Household(Agent):
    
    def __init__(self, parent=None): # Important to add default values. Here age=0
        super().__init__(parent)
        self._firm=None

    def event_proc(self, id_event):
        if id_event == Event.START: 
            return

        elif id_event == Event.PERIOD_START: 
            return

        elif id_event == Event.UPDATE:
            return                

        elif id_event == Event.PERIOD_STOP:
            if self._firm is None: # No job
                # Search  
                w , fm = [], []  
                for f in Simulation.firms.get_random_agents(n=Settings.household_search_number_of_firms):
                    if f.vacancies>0:
                        w.append(f.wage)
                        fm.append(f)

                new_firm=None
                if len(w)>0:
                    new_firm = fm[w.index(max(w))] 

                # If found a firm
                if new_firm is not None:
                    if new_firm.communicate(ECommunication.DO_YOU_HAVE_A_JOB, self)==ECommunication.YES:
                        self._firm = new_firm

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
            self._wage = Simulation.statistics.mean_wage

        self._employees = []
        self._vacancies=0

        # Random initial productivity
        self._theta = math.exp(random.gauss(Settings.firm_log_theta_initial_mean, Settings.firm_log_theta_initial_sd))
        
        # Calculate profit at the mean wage in the economy
        L_hat, Y_hat, profit_hat = self.calc_variables()
        if profit_hat > 0:
            self._vacancies = L_hat
        else:
            self.remove_this_agent() # If negative initial profit: productivity too low to live!

    def event_proc(self, id_event):
        if id_event == Event.START: 
            return

        elif id_event == Event.PERIOD_START: 
            return

        elif id_event == Event.UPDATE:
            return
   
        elif id_event == Event.PERIOD_STOP:
            alpha = Settings.firm_alpha
            p_bar = Simulation.price_bar
            L_bar = Settings.firm_min_employment

            L_hat = L_bar + (alpha*p_bar*self._theta/self._wage)**(1/(1-alpha))
            Y_hat = self._theta * (L_hat - L_bar)**alpha
            profit_hat = p_bar * Y_hat - self._wage * L_hat 

            # Random death. Just for testing
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if random.random() < 0.005:
                self.remove_this_agent()

            epsilon = random.gauss(Settings.firm_log_theta_error_mean, Settings.firm_log_theta_error_sd)
            self._theta = math.exp(math.log(self._theta) + epsilon)          
            return

    def calc_variables(self):
        alpha = Settings.firm_alpha
        p_bar = Simulation.price_bar
        L_bar = Settings.firm_min_employment

        L_hat = L_bar + (alpha*p_bar*self._theta/self._wage)**(1/(1-alpha))
        Y_hat = self._theta * (L_hat - L_bar)**alpha
        profit_hat = p_bar * Y_hat - self._wage * L_hat 

       
        
        return L_hat, Y_hat, profit_hat

    def communicate(self, e_communication, household):
        if e_communication==ECommunication.DO_YOU_HAVE_A_JOB:
            if self._vacancies>0:
                self._vacancies -= 1
                self._employees.append(household)
            return ECommunication.YES


    @property
    def wage(self):
        return self._wage

    @property
    def vacancies(self):
        return self._vacancies


    @property
    def theta(self):
        return self._theta

class Statistics(Agent):
    
    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._ts_n_households = []
            self._ts_n_firms = []
            self._ts_mean_wage = []

            self._time = None
            self._time_total = time.time()
            self._mean_wage=1

        elif id_event == Event.PERIOD_START:
            # Collect data
            self._ts_n_households.append(len(Simulation.households))
            self._ts_n_firms.append(len(Simulation.firms))

            wage = [f.wage for f in Simulation.firms] 
            theta = [f.theta for f in Simulation.firms] 
            if len(wage)>0:
                self._mean_wage = sum(wage)/len(wage)

            self._ts_mean_wage.append(self._mean_wage)


            # Show real time graphics (every graphics_periods_per_pic periode)
            show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
            last_periode = Simulation.time == Settings.number_of_periods-1            
            if show_pic or last_periode:
                plt.clf()
                plot1(self._ts_n_firms)
                plot2(theta)
                plot3(self._ts_mean_wage)
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
    
    @property
    def mean_wage(self):
        return self._mean_wage


class Simulation(Agent):
    # Static fields: Can be viewed by the other agents
    time=-1 # If time=-1 the model has not started yet.
    households=None
    firms=None
    price_bar=1  # The exogeneous international good price

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

        if id_event == Event.PERIOD_STOP:
            # New born firms
            for _ in range(Settings.firm_number_of_new_born):
                Firm(Simulation.firms)
            
            super().event_proc(id_event)
    
        # if id_event == Event.STOP:
        #     super().event_proc(id_event)


        else:
            # All other events are send to defendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------
Simulation()





