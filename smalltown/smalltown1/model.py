import random
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os
import time

from dream_agent import *

from enums import *   
from plots import *
from settings import *

# Usefull functions
def exist(x):
    return x is not None

class Household(Agent):
    
    def __init__(self, parent=None): # Important to add default values. Here age=0
        super().__init__(parent)
        self._firm=None
        self._wage_last_period=0
        self._wage=0

    def event_proc(self, id_event):
        if id_event == Event.START: 
            Settings.number_of_firms
            return

        elif id_event == Event.PERIOD_START: 
            if exist(self._firm):
                self._wage = self._firm.wage
            return

        elif id_event == Event.UPDATE:
            no_job = self._firm is None
            have_job = not no_job
            random_search = random.random() < Settings.household_probability_search  
            
            decreasing_wage=False
            if have_job:
                decreasing_wage = self._firm.wage < self._wage_last_period  

            if no_job or random_search or decreasing_wage: 
                new_firm = self.search_job()

                # If found a potential firm
                if new_firm is not None:
                    better_wage = False
                    if have_job: # If have job
                        if new_firm.wage > self._firm.wage:
                            better_wage = True

                    if no_job or better_wage:
                        if new_firm.communicate(ECommunication.DO_YOU_HAVE_A_JOB, self)==ECommunication.YES:
                            if have_job:
                                self._firm.communicate(ECommunication.I_QUIT, self)
                            self._firm = new_firm
            
            if self._firm is not None: # Remember wage
                self._wage_last_period = self._firm.wage                 
            
            return

        elif id_event == Event.PERIOD_STOP:
            return


    def communicate(self, e_communication, person):
        if e_communication==ECommunication.YOU_ARE_FIRED:
            self._firm=None
            return ECommunication.OK

    def search_job(self):
        """Returns None or a firm with a vacant job."""
        wages , firms = [], []  
        for f in Simulation.firms.get_random_agents(n=Settings.household_search_number_of_firms):
            if f.vacancies>0:
                wages.append(f.wage)
                firms.append(f)

        new_firm=None
        if len(wages)>0:
            new_firm = firms[wages.index(max(wages))] 
        
        return new_firm             


class Firm(Agent):
    
    def __init__(self, parent=None, age=0): # Important to add default values. Here age=0
        super().__init__(parent)
        if Simulation.time==-1:  # The model has not started yet
            self._wage = math.exp(random.gauss(Settings.firm_init_wage_mean, Settings.firm_init_wage_sd))   
        else:
            self._wage = Simulation.statistics.mean_wage

        self._employees = []
        self._vacancies=0
        self._reserve = Settings.firm_start_capital
        self._employed_start=0
        self._profit=0
        self._production=0
        self._default=False

        # Random initial productivity
        self._theta = math.exp(random.gauss(Settings.firm_log_theta_initial_mean, Settings.firm_log_theta_initial_sd))
        
        # Calculate profit at the mean wage in the economy
        # L_hat, Y_hat, profit_hat = self.calc_variables()
        # if profit_hat > 0:
        #     self._vacancies = L_hat
        # else:
        #     self.remove_this_agent() # If negative initial profit: productivity too low to live!

    def event_proc(self, id_event):
        if id_event == Event.START: 
            return

        elif id_event == Event.PERIOD_START: 
            self._employed_start = len(self._employees)
            return

        elif id_event == Event.UPDATE:
            if self._default:
                for h in self._employees:
                    h.communicate(ECommunication.YOU_ARE_FIRED, self)
                self.remove_this_agent()

            return
   
        elif id_event == Event.PERIOD_STOP:
            if self._default:
                self.remove_this_agent()
                return

            alpha = Settings.firm_alpha
            p     = Simulation.price
            L_min = Settings.firm_min_employment
            r     = Simulation.interest_rate

            # Observe: Production in the period is done by folks employed in the start of the period.
            # If an employed quits during the period he works to the end of the period.
            if self._employed_start >= L_min:
                self._production = self._theta * (self._employed_start - L_min) ** alpha

            # Observe: Firm pay wage to peoples employed in the start of the period (self._employed_start)
            self._profit = p * self._production - self._wage * self._employed_start

            self._reserve = (1 + r) * self._reserve + self._profit 

            # If negative reserves: DEFAULT!
            if self._reserve < 0:
                self._default=True
                return



            # L_hat = L_bar + (alpha*p_bar*self._theta/self._wage)**(1/(1-alpha))
            # Y_hat = self._theta * (L_hat - L_bar)**alpha
            # profit_hat = p_bar * Y_hat - self._wage * L_hat 

            # Random death. Just for testing
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if random.random() < 0.005:
                self.remove_this_agent()

            epsilon = random.gauss(Settings.firm_log_theta_error_mean, Settings.firm_log_theta_error_sd)
            self._theta = math.exp(math.log(self._theta) + epsilon)          
            return

    def calc_variables(self):
        """Calculates tuple: L_hat, Y_hat, profit_hat"""
        alpha = Settings.firm_alpha
        p_bar = Simulation.price
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

        elif e_communication==ECommunication.I_QUIT:
            self._employees.remove(household)
            return ECommunication.OK
    

    @property
    def wage(self):
        return self._wage

    @property
    def vacancies(self):
        """Number of vacancies"""
        return self._vacancies


    @property
    def theta(self):
        """Firms individual productivity. Follows a random walk"""
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
    price=1  # The exogeneous international good price
    interest_rate = Settings.interest_rate

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





