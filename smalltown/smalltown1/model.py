import random
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os
import time

from dream_agent import *
from tools import exist

from .enums import *   
from .plots import *
from .settings import *


class Household(Agent):
    
    def __init__(self, parent=None): # Important to add default values. Here age=0
        super().__init__(parent)
        self._firm=None
        self._wage_last_period=0
        self._wage=0
        self._search_duration=0

    def event_proc(self, id_event):
        if id_event == Event.START: 
            return

        elif id_event == Event.PERIOD_START: 
            if exist(self._firm):
                self._wage_last_period = self._wage                    
                self._wage = self._firm.wage
            return

        elif id_event == Event.UPDATE:
            have_job        = exist(self._firm)
            no_job          = not have_job 
            random_search   = random.random() < Settings.household_probability_search             
            
            decreasing_wage = False
            below_mean=False
            if exist(self._firm):
                decreasing_wage = True if self._firm.wage < self._wage_last_period else False
                below_mean = True if self._firm.wage < Simulation.statistics.mean_wage else False
            
            # if no_job or random_search or decreasing_wage or below_mean: 
            if no_job or random_search or below_mean: 
                new_firm = self.search_job()

                # If found a potential firm
                if exist(new_firm):
                    better_wage = False
                    if have_job: # If have job
                        if new_firm.wage > self._firm.wage:
                            better_wage = True

                    if no_job or better_wage:
                        if new_firm.communicate(ECommunication.DO_YOU_HAVE_A_JOB, self)==ECommunication.YES:
                            if have_job:
                                self._firm.communicate(ECommunication.I_QUIT, self)
                            self._firm = new_firm
                    self._search_duration = 0
                else:
                    self._search_duration += 1            
            return

        elif id_event == Event.PERIOD_STOP:
            return


    def communicate(self, e_communication, firm):
        if e_communication==ECommunication.YOU_ARE_FIRED:
            self._firm=None
            return ECommunication.OK

    def search_job(self):
        """Returns None or a firm with a vacant job."""
        w_best=-1
        new_firm=None
        for f in Simulation.firms.get_random_agents(n=Settings.household_search_number_of_firms):
            if f.vacancies>0:
                if f.wage > w_best:
                    w_best   = f.wage
                    new_firm = f
        
        return new_firm             

    @property
    def search_duration(self):
        return self._search_duration



class Firm(Agent):
    
    def __init__(self, parent=None,age=0): # Important to add default values. Here age=0
        super().__init__(parent)
        if Simulation.time==-1:  # The model has not started yet
            self._wage = math.exp(random.gauss(Settings.firm_init_wage_mean, Settings.firm_init_wage_sd))  
            self._reserve = random.uniform(Settings.firm_credit_limit,0)  # Just do get a smooth development in the burn-in-period
        else:
            self._wage = Simulation.statistics.mean_wage # New firm at run-time
            # self._wage = random.gauss(Simulation.statistics.mean_wage, 0.2) # New firm at run-time
            self._reserve = 0

        self._age = age
        self._employees = []
        self._vacancies = Settings.firm_initial_vacancies
        self._reserve_target=0
        self._withdrawal=0
        self._employed_start=0
        self._profit=0
        self._production=0
        self._default=False

        # Random initial productivity
        mean = Settings.firm_log_theta_initial_mean
        sd   = Settings.firm_log_theta_initial_sd
        # self._theta = math.exp(random.gauss(mean, sd))
        self._theta = random.gauss(mean, sd)
        if self._theta < 1e-4:
            self._theta = 1e-4
        
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
            alpha = Settings.firm_alpha
            zeta  = Settings.firm_reserve_target_wagesum_parameter
            gamma = Settings.firm_buffer_stock_speed
            p     = Simulation.price
            L_min = Settings.firm_min_employment
            r     = Simulation.interest_rate
            w_bar = Simulation.statistics.mean_wage
           
            # Observe: Production in the period is done by folks employed in the start of the period.
            # If an employed quits during the period he works to the end of the period.
            if self._employed_start >= L_min:
                self._production = self._theta * (self._employed_start - L_min) ** alpha
            else:
                self._production = 0

            # Observe: Firm pay wage to peoples employed in the start of the period (self._employed_start)
            self._profit = p * self._production - self._wage * self._employed_start

            self._reserve_target = zeta * self._wage * self._employed_start
            buffer_stock_saving = gamma * (self._reserve_target - self._reserve) - r * self._reserve
           
            if self._profit > buffer_stock_saving:
                self._saving = buffer_stock_saving
            else:
                self._saving = self._profit

            self._withdrawal = self._profit - self._saving

            self._reserve = (1 + r) * self._reserve + self._saving 

            # If too much dept: DEFAULT!
            if self._age>50 and len(self._employees)==0:
                self._default=True
                return

            if self._reserve < Settings.firm_credit_limit:
                self._default=True
                return
      
            if Simulation.time>200:
                zz=22

            L_opt = self.calculate_optimal_employment(self._wage)
            L = len(self._employees)

            self._vacancies=0
            if L_opt > L:
                if L>1:
                    self._wage = (1 + Settings.firm_wage_markup) * self._wage
                else:
                    self._wage = self._wage

                self._vacancies = L_opt - L  
            elif L_opt == L: 
                self._wage = self._wage
            elif L_opt < L:
                self._wage = self._wage / (1 + Settings.firm_wage_markdown)

            epsilon = random.gauss(Settings.firm_log_theta_error_mean, Settings.firm_log_theta_error_sd)
            # self._theta = math.exp(math.log(self._theta) + epsilon)          
            self._theta = self._theta + epsilon          
            if self._theta < 1e-4:
                self._theta = 1e-4
            self._age += 1
            return

    def calculate_optimal_employment(self, wage):
        alpha = Settings.firm_alpha
        p     = Simulation.price
        L_min = Settings.firm_min_employment
           
        profit0 = -1e9
        L_opt=None
        for L in range(L_min, 1000):            
            y = self._theta * (L - L_min) ** alpha
            profit = p * y - wage * L
            if profit < profit0:
                L_opt = L-1                    
                break
            profit0 = profit

        return L_opt

    def calc_variables(self):
        """Calculates wage and optimal employment L_hat

        Returns:
            tuple: wage, L_hat. If no employment: Returns w_bar and optimal L_hat given w=w_bar 
        """
        alpha = Settings.firm_alpha
        E = Settings.firm_wage_reaction
        p = Simulation.price
        L_min = Settings.firm_min_employment
        w_bar = Simulation.statistics.mean_wage
        L0 = len(self._employees)

        if L0==0: # If no employment: Returns w_bar and optimal L_hat given w=w_bar 
            w = w_bar
            L_hat = L_min + (alpha*p*self._theta/w)**(1/(1-alpha))                
            return w, L_hat

        # Iterations
        L_hat0, itt = 0, 0
        w = w_bar # Start value
        for _ in range(Settings.firm_calc_variables_max_iterations):
            L_hat = L_min + (alpha*p*self._theta/w)**(1/(1-alpha))                
            w = w_bar * (L_hat / L0) ** E
            if abs(L_hat-L_hat0) < Settings.firm_calc_variables_error_ok:
                break
            L_hat0 = L_hat
            itt += 1                    

        return w, L_hat

    def communicate(self, e_communication, household):
        if e_communication==ECommunication.DO_YOU_HAVE_A_JOB:
            if self._vacancies>0:
                self._vacancies -= 1
                self._employees.append(household)
                return ECommunication.YES
            else:
                return ECommunication.NO

        elif e_communication==ECommunication.I_QUIT:
            self._employees.remove(household)
            return ECommunication.OK
    

    @property
    def age(self):
        return self._age

    @property
    def wage(self):
        return self._wage

    @property
    def vacancies(self):
        """Number of vacancies"""
        return self._vacancies

    @property
    def employment(self):
        """Number of employed"""
        return len(self._employees)

    @property
    def theta(self):
        """Firms individual productivity. Follows a random walk"""
        return self._theta

    @property
    def profit(self):
        """Firms profit"""
        return self._profit

    @property
    def reserve(self):
        """Firms reserve"""
        return self._reserve

    @property
    def production(self):
        """Firms production"""
        return self._production

    @property
    def default(self):
        """True if firms has defaulted"""
        return self._default

class Statistics(Agent):
    
    def event_proc(self, id_event):
        if id_event == Event.START:
            graphics_init() # Initialize graphics
            self._ts_n_households = []
            self._ts_n_firms = []
            self._ts_n_employed = []
            self._ts_n_defaults = []
            self._ts_mean_wage = []
            self._ts_total_production = []

            self._time = None
            self._time_total = time.time()
            self._mean_wage=1.0

        elif id_event == Event.PERIOD_START:
            # Collect data
            self._ts_n_households.append(len(Simulation.households))
            self._ts_n_firms.append(len(Simulation.firms))

            t = Simulation.time

            L_sum=0
            w_sum=0 
            w_n=0
            Y_sum=0
            n_defaults=0
            for f in Simulation.firms:
                if exist(f.wage): 
                    w_sum += f.wage
                    w_n += 1               
                L_sum += f.employment
                Y_sum += f.production
                if f.default:
                    n_defaults += 1

            if w_n>0:
                self._mean_wage = w_sum/w_n

            self._ts_mean_wage.append(self._mean_wage)
            self._ts_n_employed.append(L_sum)
            self._ts_total_production.append(Y_sum)
            self._ts_n_defaults.append(n_defaults)

            if Settings.graphics_show:
                # Show real time graphics (every graphics_periods_per_pic periode)
                show_pic     = Simulation.time % Settings.graphics_periods_per_pic==0
                last_periode = Simulation.time == Settings.number_of_periods-1            
                if show_pic or last_periode:

                    theta = [i for i in range(len(Simulation.firms)) ] 
                    profit = [i for i in range(len(Simulation.firms))] 
                    reserve = [i for i in range(len(Simulation.firms))]            
                    vacancies = [i for i in range(len(Simulation.firms))]
                    wage = [i for i in range(len(Simulation.firms))] 
                    employment = [i for i in range(len(Simulation.firms))] 
                    
                    search_duration = [i for i in range(len(Simulation.households))]
                
                    i=0
                    for f in Simulation.firms:
                        theta[i] = f.theta
                        profit[i] = f.profit
                        reserve[i] = f.reserve
                        vacancies[i] = f.vacancies                
                        wage[i] = f.wage
                        employment[i] = f.employment
                        i += 1

                    i=0
                    for h in Simulation.households:
                        search_duration[i] = h.search_duration
                        i += 1

                    plt.clf()
                    plot1(self._ts_n_firms)
                    plot2(theta)
                    plot3(self._ts_mean_wage)
                    plot4(self._ts_n_employed)
                    plot5(profit)
                    plot6(reserve)
                    plot7(wage)
                    plot8(search_duration)
                    plot9(vacancies)
                    plot10(employment)
                    plot11(self._ts_total_production)
                    plot12(self._ts_n_defaults)
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
    price = Settings.price  # The exogeneous international good price
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
            if random.random() < 0.2: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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





